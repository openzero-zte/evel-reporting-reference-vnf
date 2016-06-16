#!/usr/bin/env python
'''
Class for Syslog Events.

Encapsulates the syslog-specific info specified in the API.

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
import logging
from event import Event, EventJSONEncoder

logger = logging.getLogger('backend.sys')

class Syslog(Event):
    '''
    Vendor Event Listener - Fault class.

    This class wraps the functionality required of syslog events and broadly
    corresponds to the syslogFields definition in the Vendor Event Listener
    API specification.
    '''

    def __init__(self, event_id, vm_id, vm_name, vf_status='Active'):
        '''
        Constructor of the Event.

        Initializes the yslog's state deriving the VM information from that
        passed in (typically by the EventManager) and passing that information
        to the Event class we're derived from. Most of the Fault's properties
        are initialized to be empty and may then be set by the instantiator of
        the object.
        '''

        super(Syslog, self).__init__(event_id, vm_id, vm_name, vf_status)
        self.domain = u'syslog'

        #----------------------------------------------------------------------
        # required fields
        #----------------------------------------------------------------------
        self.event_source_type = u'virtualMachine(8)'
        self.syslog_tag = u''
        self.syslog_msg = u''

        #----------------------------------------------------------------------
        # optional fields
        #----------------------------------------------------------------------
        self.event_source_host = None
        self.syslog_facility = None
        self.syslog_proc = None
        self.syslog_proc_id = None
        self.syslog_ver = None
        self.syslog_sdata = None
        self.syslog_fields_version = 1

    def encode_json(self):
        '''
        Encode the Syslog as JSON.

        Returns a string with the encoded JSON.
        '''
        return json.dumps(self, cls=SyslogJSONEncoder)

    def __unicode__(self):
        '''Provide a human-readable dump of the Syslog's state.
        '''
        s = super(Syslog, self).__unicode__()
        s += u'\nSyslog Header\n'
        s += u'============\n'
        s += u'    Event source type: {}\n'.format(self.event_source_type)
        s += u'    Tag: {}\n'.format(self.syslog_tag)
        s += u'    Message: {}\n'.format(self.syslog_msg)
        s += u'    Host: {}\n'.format(self.event_source_host)
        s += u'    Facility: {}\n'.format(self.syslog_facility)
        s += u'    Proc.: {}\n'.format(self.syslog_proc)
        s += u'    Proc ID: {}\n'.format(self.syslog_proc_id)
        s += u'    Version: {}\n'.format(self.syslog_ver)
        s += u'    SData: {}\n'.format(self.syslog_sdata)
        s += u'    Fields Version: {}\n'.format(self.syslog_fields_version)
        return s

    def __str__(self):
        '''
        Provide a human readable dump of the Syslog's state encoded as UTF-8.
        '''
        return unicode(self).encode('utf-8')

class SyslogJSONEncoder(EventJSONEncoder):
    '''Specialization of the JSONEncoder to encode Syslog events.
    '''
    def default(self, obj):
        '''
        Encode the supplied object, first checking it really is an Fault.

        Any error handling is deferred to the base-class's handling.
        '''
        if isinstance(obj, Syslog):
            #------------------------------------------------------------------
            # Convert the Syslog into a dictionary which matches the JSON
            # object that definition in the Vendor Event Listener API
            # specification.
            #------------------------------------------------------------------
            logger.info('encoding syslog')
            vel_dict = EventJSONEncoder.default(self, obj)
            vel_dict['event']['syslogFields'] = {}
            vel_dict['event']['syslogFields']['eventSourceType'] = \
                                                          obj.event_source_type
            vel_dict['event']['syslogFields']['syslogTag'] = obj.syslog_tag
            if obj.syslog_msg:
                vel_dict['event']['syslogFields']['syslogMsg'] = obj.syslog_msg
            if obj.event_source_host:
                vel_dict['event']['syslogFields']['eventSourceHost'] = \
                                                          obj.event_source_host
            if obj.syslog_facility:
                vel_dict['event']['syslogFields']['syslogFacility'] = \
                                                            obj.syslog_facility
            if obj.syslog_proc:
                vel_dict['event']['syslogFields']['syslogProc'] = \
                                                                obj.syslog_proc
            if obj.syslog_proc_id:
                vel_dict['event']['syslogFields']['syslogProcId'] = \
                                                             obj.syslog_proc_id
            if obj.syslog_ver:
                vel_dict['event']['syslogFields']['syslogVer'] = obj.syslog_ver
            if obj.syslog_sdata:
                vel_dict['event']['syslogFields']['syslogSData'] = \
                                                               obj.syslog_sdata
            if obj.syslog_fields_version:
                vel_dict['event']['syslogFields']['syslogFieldsVersion'] = \
                                                      obj.syslog_fields_version
            logger.info('syslog encoded as: {}'.format(vel_dict))
        return vel_dict

        #----------------------------------------------------------------------
        # The object isn't of the expected type - it let the base encoder do
        # the work of raising the exception.
        #----------------------------------------------------------------------
        logger.error('Syslog JSON encoder can\'t handle object: {}' \
                                                                 .format(obj))
        return json.JSONEncoder.default(self, obj)
