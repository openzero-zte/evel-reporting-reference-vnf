#!/usr/bin/env python
'''
Wraps the JSON API to the AT&T Event Collector service.

License
-------

Copyright(c) <2016>, AT&T Intellectual Property.  All other rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
3. All advertising materials mentioning features or use of this software
   must display the following acknowledgement:  This product includes
   software developed by the AT&T.
4. Neither the name of AT&T nor the names of its contributors may be used to
   endorse or promote products derived from this software without specific
   prior written permission.

THIS SOFTWARE IS PROVIDED BY AT&T INTELLECTUAL PROPERTY ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL AT&T INTELLECTUAL PROPERTY BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

from threading import Thread
from Queue import Queue
import logging
import base64
import urllib2

from metadata import OpenstackMetadataService
from measurement_event import Measurement
from fault_event import Fault
from event import Event
from mobile_flow_event import MobileFlow
from syslog_event import Syslog

logger = logging.getLogger('backend.em')

event_manager = None

class EventManager(object):
    '''
    Manage events being sent to the Vendor Event Listener service.

    This class should be instantiated as a singleton and is then responsible
    for sending events to the Vendor Event Listener. The Event Manager runs a
    notification thread which listens for events to be sent on an inter-thread
    queue, which are then sent over the JSON interface to the Vendor Event
    Listener.

    The instance is also used as a factory for Events, Faults, Measurements and
    Heartbeats ensuring that they get allocated appropriate sequence numbers.
    '''
    API_VERSION = 1

    def __init__(self,
                 domain,
                 port,
                 path,
                 username,
                 password,
                 topic_name='',
                 use_https=True):
        '''
        Construct the Event Manager

        Sets up the Event Manager's internal state. Note that a significant
        amount of information needs to be cached from the OpenStack
        environment. If that environment appears not to be available, the
        information will be spoofed to enable the system to work outside of
        OpenStack for development/test purposes
        '''

        #----------------------------------------------------------------------
        # Set up the internal state of the Event Manager.
        #----------------------------------------------------------------------
        self.event_id = 0
        self.topic_name = topic_name
        self.use_https = use_https
        self.vnf_state = 'Active'
        self.time_to_terminate = 0

        #======================================================================
        # Extract information from the OpenStack metadata service.  If present,
        # information about the Vendor Event Listener takes precedence over
        # that in the local config file.
        #======================================================================
        metadata = OpenstackMetadataService()
        self.vm_name = metadata.name
        self.vm_id = metadata.uuid
        if ('meta' in metadata.metadata):
            logger.debug('OpenStack does have some user metadata available')
            if ('vel_domain' in metadata.metadata['meta']):
                domain = metadata.metadata['meta']['vel_domain']
                logger.debug('Extracted domain "{}" '
                             'from metadata service'.format(domain))
            if ('vel_port' in metadata.metadata['meta']):
                port = metadata.metadata['meta']['vel_port']
                logger.debug('Extracted port "{}" '
                             'from metadata service'.format(port))
            if ('vel_path' in metadata.metadata['meta']):
                path = metadata.metadata['meta']['vel_path']
                logger.debug('Extracted path "{}" '
                             'from metadata service'.format(path))
            if ('vel_username' in metadata.metadata['meta']):
                username = metadata.metadata['meta']['vel_username']
                logger.debug('Extracted username "{}" '
                             'from metadata service'.format(username))
            if ('vel_password' in metadata.metadata['meta']):
                password = metadata.metadata['meta']['vel_password']
                logger.debug('Extracted password "{}" '
                             'from metadata service'.format(password))
            if ('vel_topic_name' in metadata.metadata['meta']):
                topic_name = metadata.metadata['meta']['vel_topic_name']
                logger.debug('Extracted topic name "{}" '
                             'from metadata service'.format(topic_name))
        else:
            logger.info('OpenStack does not have user metadata available.  '
                        'Using config from file instead')

        #======================================================================
        # Build the derived values we need for our operation.
        #======================================================================
        self.server_url = 'http{}://{}:{}/{}eventListener/v{}{}'.format(
                                                    's' if use_https else '',
                                                    domain,
                                                    port,
                                                    path,
                                                    EventManager.API_VERSION,
                                                    '/' + topic_name
                                                        if len(topic_name) > 0
                                                        else '')
        logger.info('Vendor Event Listener is at: {}'.format(self.server_url))
        self.credentials = base64.b64encode('{}:{}'.format(username, password))
        logger.debug('Authentication credentials are: {}'.format(
                                                             self.credentials))
        return

    def start(self):
        '''
        Start a thread which listens for work to dispatch to the server.

        Note that we process each request to completion so that the collector
        will see the requests serialized from a given instance.
        '''
        logger.info('Starting Event Manager...')
        self.queue = Queue()
        self.manager_thread = Thread(target=self.listener)
        self.manager_thread.daemon = True
        self.manager_thread.start()

    def listener(self):
        '''
        Listen for events to send to the Vendor Event Listener service.
        '''
        logger.info('Started Event Listener')
        while True:
            data = self.queue.get()
            print('Listener got data:\n{}'.format(data))
            logger.debug(u'Listener got data:\n{}'.format(data))

            #------------------------------------------------------------------
            # Post the event to the correct URL for the topic (eventType),
            # if we're using topic-based URLs.  Note that we can't make any
            # assumptions about the topics, so make sure that they're "safe" as
            # URL paths.
            #------------------------------------------------------------------
            try:
                event_data = data.encode_json()
                rest_url = self.server_url
                logger.debug('Sending "{}" to "{}"'.format(event_data,
                                                           rest_url))
                request = urllib2.Request(rest_url)
                request.add_header('Authorization', 'Basic {}'.format(
                                                             self.credentials))
                request.add_header('Content-Type', 'application/json')
                vel = urllib2.urlopen(request, event_data, timeout=1)

                #--------------------------------------------------------------
                # Process the response - we expect a 204 No Content normally.
                #--------------------------------------------------------------
                response_code = vel.getcode()
                logger.debug('Response code is: {}'.format(response_code))
                if response_code == 204:
                    logger.debug('Good response')
                else:
                    logger.warning('Unexpected response')
                    response = vel.read()
                    logger.debug(u'Vendor Event Listener response body is: '
                                 u'{}'.format(response))

            except urllib2.HTTPError as e:
                #--------------------------------------------------------------
                # We seem to be able to talk to the service, but we got a
                # failure code.  Extract any exception information.
                #--------------------------------------------------------------
                logger.warning('Vendor Event Listener returned {}.'.format(
                                                                       e.code))
                response = e.read()
                logger.debug('Vendor Event Listener response body is: '
                             '{}'.format(response))

            except urllib2.URLError as e:
                #--------------------------------------------------------------
                # Assume that the VEL service is down at the moment, so log the
                # failure.
                #--------------------------------------------------------------
                logger.warning('Vendor Event Listener is is not reachable: {}.'
                               '\nEvent will be lost: {}'.format(e, data))

    def new_event(self):
        '''
        Make a new Event, getting the required information for the constructor
        from the information about the environment cached in the EventManager.
        '''

        self.event_id += 1
        return Event(self.event_id, self.vm_id, self.vm_name, self.vnf_state)

    def new_fault(self):
        '''
        Make a new Fault, getting the required information for the constructor
        from the information about the environment cached in the EventManager.
        '''

        self.event_id += 1
        return Fault(self.event_id, self.vm_id, self.vm_name, self.vnf_state)

    def new_measurement(self):
        '''
        Make a new Measurement, getting the required information for the
        constructor from the information about the environment cached in the
        EventManager.
        '''

        self.event_id += 1
        return Measurement(self.event_id,
                           self.vm_id,
                           self.vm_name,
                           self.vnf_state)

    def new_mobile_flow(self):
        '''
        Make a new Mobile Flow, getting the required information for the
        constructor from the information about the environment cached in the
        EventManager.
        '''

        self.event_id += 1
        return MobileFlow(self.event_id,
                          self.vm_id,
                          self.vm_name,
                          self.vnf_state)

    def new_syslog(self):
        '''
        Make a new Syslog, getting the required information for the constructor
        from the information about the environment cached in the EventManager.
        '''

        self.event_id += 1
        return Syslog(self.event_id, self.vm_id, self.vm_name, self.vnf_state)

    def new_heartbeat(self):
        '''
        Make a new Heartbeat, getting the required information for
        the constructor from the information about the environment cached in
        the EventManager.
        '''

        heartbeat = self.new_event()
        heartbeat.domain = 'heartbeat'
        return heartbeat

    def post_event(self, event):
        '''Post an event onto the internal queue.'''
        self.queue.put(event)

    def prepare_terminate(self, dwell_time):
        '''Prepare to terminate the VNF.

        Simulate orderly shutdown of a VNF.  Just implements a delayed state
        change. The state change from **Preparing to Terminate** to
        **Ready to Terminate** will happen after *dwell_time* seconds.
        *dwell_time* should be an integer.
        '''
        logger.info('VNF preparing to terminate from {} in {} secs'.format(
                                                               self.vnf_state,
                                                               dwell_time))

        #======================================================================
        # Update the VNF state.
        #======================================================================
        self.time_to_terminate = dwell_time
        self.vnf_state = 'Preparing to terminate'

        #======================================================================
        # Generate a gratuitous heartbeat to notify the collector of the state-
        # change.
        #======================================================================
        event = self.new_heartbeat()
        self.post_event(event)

        return

    def set_active(self):
        '''Sets the VNF back to its active state.

        Can be used after the "Prepare Terminate" state changes to revert back
        to the Active state.
        '''

        #======================================================================
        # Update the VNF state.
        #======================================================================
        self.vnf_state = 'Active'
        self.time_to_terminate = 0

        #======================================================================
        # Generate a gratuitous heartbeat to notify the collector of the state-
        # change.
        #======================================================================
        event = self.new_heartbeat()
        self.post_event(event)

        return

    def update_vnf_state(self):
        ''' Update VNF State

        Called once per second bye the foreground main-loop in order to manage
        state transitions.
        '''

        #======================================================================
        # Check whether we're in the Preparing to Terminate state and if we
        # are then manage the "dwell" time until we enter the Ready to
        # Terminate state.
        #======================================================================
        if (self.vnf_state == 'Preparing to terminate'):
            logger.debug('Preparing to terminate in {} secs'.format(
                                                        self.time_to_terminate))
            if (self.time_to_terminate == 0):
                logger.info('Preparations to terminate are complete!  '
                            'Transition to Ready to Terminate state.')

                #==========================================================
                # Update the state.
                #==========================================================
                self.vnf_state = 'Ready to terminate'

                #==========================================================
                # Generate a gratuitous heartbeat to notify the collector
                # of the state-change.
                #==========================================================
                event = self.new_heartbeat()
                self.post_event(event)
            self.time_to_terminate -= 1

        return

def create_event_manager(domain,
                         port,
                         path,
                         username,
                         password,
                         use_topic_urls,
                         use_https):
    '''Create an EventManager

    Creates the singleton EventManager (checking it really is a singleton).
    '''

    global event_manager
    if (event_manager is None):
        event_manager = EventManager(domain,
                                     port,
                                     path,
                                     username,
                                     password,
                                     use_topic_urls,
                                     use_https)
        logger.debug('Created EventManager instance')
    else:
        raise RuntimeError('Tried to instantiate multiple EventManager'
                           ' instances! Only one can be created')
    return event_manager

def get_event_manager():
    '''
    Return a reference to the singleton EventManager (checking it has been
    created properly first.)
    '''

    global event_manager
    if (event_manager is None):
        raise RuntimeError('No EventManager instance has been created!')
    return event_manager
