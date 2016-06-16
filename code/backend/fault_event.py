#!/usr/bin/env python
'''
Class for Faults.

Encapsulates the fault-specific info specified in the API.

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

logger = logging.getLogger('backend.flt')

class Fault(Event):
    '''
    Vendor Event Listener - Fault class.

    This class wraps the functionality required of Fault events and broadly
    corresponds to the faultFields definition in the Vendor Event Listener
    API specification.
    '''
    'Definition: severity'
    SEVERITY_CRITICAL = 'CRITICAL'
    SEVERITY_MAJOR = 'MAJOR'
    SEVERITY_MINOR = 'MINOR'
    SEVERITY_WARNING = 'WARNING'
    SEVERITY_NORMAL = 'NORMAL'

    def __init__(self, event_id, vm_id, vm_name, vf_status='Active'):
        '''
        Constructor of the Event.

        Initializes the Fault's state deriving the VM information from that
        passed in (typically by the EventManager) and passing that information
        to the Event class we're derived from. Most of the Fault's properties
        are initialized to be empty and may then be set by the instantiator of
        the object.
        '''

        super(Fault, self).__init__(event_id, vm_id, vm_name, vf_status)
        self.domain = u'fault'

        #----------------------------------------------------------------------
        # required fields
        #----------------------------------------------------------------------
        self.alarm_condition = u''
        self.event_severity = Fault.SEVERITY_NORMAL
        self.event_source_type = u'virtualMachine(8)'
        self.specific_problem = u''

        #----------------------------------------------------------------------
        # optional fields
        #----------------------------------------------------------------------
        self.alarm_additional_info = []
        self.alarm_a_interface = None
        self.fault_fields_version = 1


    def encode_json(self):
        '''
        Encode the Fault as JSON.

        Returns a string with the encoded JSON.
        '''
        return json.dumps(self, cls=FaultJSONEncoder)

    def __unicode__(self):
        '''Provide a human-readable dump of the Fault's state.'''
        s = super(Fault, self).__unicode__()
        s += u'\nFault Header\n'
        s += u'============\n'
        for addl_info in self.alarm_additional_info:
            s += u' Alarm Additional Info: {}: {}\n'.format(addl_info[0],
                                                            addl_info[1])
        s += u'       Alarm Condition: {}\n'.format(self.alarm_condition)
        s += u'     Alarm A Interface: {}\n'.format(self.alarm_a_interface)
        s += u'        Alarm Severity: {}\n'.format(self.event_severity)
        s += u'     Event Source Type: {}\n'.format(self.event_source_type)
        s += u'  Fault Fields Version: {}\n'.format(self.fault_fields_version)
        s += u'      Specific Problem: {}\n'.format(self.specific_problem)
        s += u'             VF Status: {}\n'.format(self.vf_status)
        return s

    def __str__(self):
        '''
        Provide a human readable dump of the Event's state encoded as UTF-8.
        '''
        return unicode(self).encode('utf-8')

class FaultJSONEncoder(EventJSONEncoder):
    '''Specialization of the JSONEncoder to encode Faults.'''
    def default(self, obj):
        '''
        Encode the supplied object, first checking it really is an Fault.

        Any error handling is deferred to the base-class's handling.
        '''
        if isinstance(obj, Fault):
            #------------------------------------------------------------------
            # Convert the Fault into a dictionary which matches the JSON object
            # that definition in the Vendor Event Listener API specification.
            #------------------------------------------------------------------
            vel_dict = EventJSONEncoder.default(self, obj)
            vel_dict['event']['faultFields'] = {}
            if len(obj.alarm_additional_info) > 0:
                vel_dict['event'][
                         'faultFields']['alarmAdditionalInformation'] = \
                                    [{'name': info[0],
                                      'value': info[1]} for info in
                                                    obj.alarm_additional_info]
            vel_dict['event']['faultFields']['alarmCondition'] = \
                                                    obj.alarm_condition
            if obj.alarm_a_interface:
                vel_dict['event']['faultFields']['alarmInterfaceA'] = \
                                                    obj.alarm_a_interface
            vel_dict['event']['faultFields']['eventSeverity'] = \
                                                    obj.event_severity
            vel_dict['event']['faultFields']['eventSourceType'] = \
                                                    obj.event_source_type
            vel_dict['event']['faultFields']['faultFieldsVersion'] = \
                                                    obj.fault_fields_version
            vel_dict['event']['faultFields']['specificProblem'] = \
                                                    obj.specific_problem
            vel_dict['event']['faultFields']['vfStatus'] = \
                                                    obj.vf_status

            logger.info('Fault encoded as: {}'.format(vel_dict))
            return vel_dict

        #----------------------------------------------------------------------
        # The object isn't of the expected type - it let the base encoder do
        # the work of raising the exception.
        #----------------------------------------------------------------------
        logger.error('Fault JSON encoder can\'t handle object: {}'.format(obj))
        return json.JSONEncoder.default(self, obj)
