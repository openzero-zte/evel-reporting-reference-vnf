#!/usr/bin/env python
'''
Base class for all types of events.

Encapsulates the header specified in the API.

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

import json
import time

global logger

class Event(object):
    '''
    Vendor Event Listener - base Event class.
    
    This class wraps the functionality required of all event types (Faults,
    Measurements *etc*) and broadly corresponds to the eventHeader definition 
    in the Vendor Event Listener API specification.
    '''

    'Definitions: fuctionalRole'
    FUNCTIONAL_ROLE_unknown = 'unknown'
    FUNCTIONAL_ROLE_eNodeB = 'eNodeB'
    FUNCTIONAL_ROLE_MME = 'MME'
    FUNCTIONAL_ROLE_PCRF = 'PCRF'

    'Definitions: priority'
    PRIORITY_HIGH = 'High'
    PRIORITY_MEDIUM = 'Medium'
    PRIORITY_NORMAL = 'Normal'
    PRIORITY_LOW = 'Low'

    def __init__(self,
                 event_id,
                 vm_id,
                 vm_name,
                 vf_status='Active',
                 functional_role=FUNCTIONAL_ROLE_unknown):
        '''
        Constructor of the Event.
        
        Initializes the Event's state deriving the VM information from that 
        passed in (typically by the EventManager) and deriving the timestamps
        from the current time.
        '''
        #----------------------------------------------------------------------
        # Current time
        #----------------------------------------------------------------------
        now = int(time.time() * 1e6)

        self.domain = u''
        self.event_id = event_id
        self.event_type = u''
        self.functional_role = functional_role
        self.last_epoch_microsec = now
        self.priority = Event.PRIORITY_NORMAL
        self.reporting_entity_id = vm_id
        self.reporting_entity_name = vm_name
        self.sequence = 0
        self.source_id = vm_id
        self.source_name = vm_name
        self.start_epoch_microsec = now
        self.version = 1
        self.vf_status = vf_status

    def encode_json(self):
        '''
        Encode the Event as JSON.
        
        Returns a string with the encoded JSON.
        '''
        return json.dumps(self, cls=EventJSONEncoder)

    def __unicode__(self):
        '''Provide a human-readable dump of the Event's state.'''
        s = u'Event Header\n'
        s += u'============\n'
        s += u'                Domain: {}\n'.format(self.domain)
        s += u'              Event ID: {}\n'.format(self.event_id)
        s += u'            Event Type: {}\n'.format(self.event_type)
        s += u'       Functional Role: {}\n'.format(self.functional_role)
        s += u' Last Epoch (microsec): {:d}\n'.format(self.last_epoch_microsec)
        s += u'              Priority: {}\n'.format(self.priority)
        s += u'   Reporting Entity ID: {}\n'.format(self.reporting_entity_id)
        s += u' Reporting Entity Name: {}\n'.format(self.reporting_entity_name)
        s += u'              Sequence: {}\n'.format(self.sequence)
        s += u'             Source ID: {}\n'.format(self.source_id)
        s += u'           Source Name: {}\n'.format(self.source_name)
        s += u'Start Epoch (microsec): {:d}\n'.format(self.start_epoch_microsec)
        s += u'               Version: {}\n'.format(self.version)

        return s

    def __str__(self):
        '''
        Provide a human readable dump of the Event's state encoded as UTF-8.
        '''
        return unicode(self).encode('utf-8')

class EventJSONEncoder(json.JSONEncoder):
    '''Specialization of the JSONEncoder to encode Events.'''
    def default(self, obj):
        '''
        Encode the supplied object, first checking it really is an Event.
        
        Any error handling is deferred to the base-class's handling.
        '''
        if isinstance(obj, Event):
            #------------------------------------------------------------------
            # Convert the event into a dictionary which matches the JSON object
            # that definition in the Vendor Event Listener API specification.
            #------------------------------------------------------------------
            vel_dict = {}
            vel_dict['domain'] = obj.domain
            vel_dict['eventId'] = str(obj.event_id)
            if obj.event_type != '': vel_dict['eventType'] = obj.event_type
            vel_dict['functionalRole'] = obj.functional_role
            vel_dict['lastEpochMicrosec'] = obj.last_epoch_microsec
            vel_dict['priority'] = obj.priority
            vel_dict['reportingEntityId'] = obj.reporting_entity_id
            vel_dict['reportingEntityName'] = obj.reporting_entity_name
            vel_dict['sequence'] = obj.sequence
            vel_dict['sourceId'] = obj.source_id
            vel_dict['sourceName'] = obj.source_name
            vel_dict['startEpochMicrosec'] = obj.start_epoch_microsec
            vel_dict['version'] = obj.version

            return {'event': {'commonEventHeader': vel_dict}}

        #----------------------------------------------------------------------
        # The object isn't of the expected type - it let the base encoder do
        # the work of raising the exception.
        #----------------------------------------------------------------------
        logger.error('Event JSON encoder can\'t handle object: {}'.format(obj))
        return json.JSONEncoder.default(self, obj)
