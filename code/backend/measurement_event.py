#!/usr/bin/env python
'''
Class for Measurements.

Encapsulates the measurement-specific info specified in the API.

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

logger = logging.getLogger('backend.meas')

class Measurement(Event):
    '''
    Vendor Event Listener - Measurement class.

    This class wraps the functionality required of Measurement events and
    broadly corresponds to the faultFields definition in the Vendor Event
    Listener API specification.
    '''
    def __init__(self, event_id, vm_id, vm_name, vf_status='Active'):
        '''
        Constructor of the Event.

        Initializes the Measurement's state deriving the VM information from
        that passed in (typically by the EventManager) and passing that
        information to the Event class we're derived from. Most of the
        Measurement's properties are initialized to be empty and may then be
        set by the instantiator of the object.
        '''
        super(Measurement, self).__init__(event_id,
                                          vm_id,
                                          vm_name,
                                          vf_status='Active')

        self.domain = u'measurementsForVfScaling'

        #----------------------------------------------------------------------
        # required
        #----------------------------------------------------------------------
        self.concurrent_sessions = 0
        self.configured_entities = 0
        self.cpu_use = []
        self.file_system_use = []
        self.latency_distribution = []
        self.mean_request_latency = 0.0
        self.measurement_interval = 0.0
        self.memory_configured = 0.0
        self.memory_used = 0.0
        self.request_rate = 0
        self.vnic_use = []

        #----------------------------------------------------------------------
        # optional
        #----------------------------------------------------------------------
        self.aggregate_cpu_usage = None
        self.measurement_fields_version = 1
        self.media_ports_in_use = None
        self.scaling_metric = None
        self.additional_measurement_groups = []
        self.codecs_in_use = []
        self.features_in_use = []
        return

    def encode_json(self):
        '''
        Encode the Fault as JSON.

        Returns a string with the encoded JSON.
        '''
        return json.dumps(self, cls=MeasurementJSONEncoder)

    def __unicode__(self):
        '''Provide a human-readable dump of the Measurement's state.'''
        s = super(Measurement, self).__unicode__()
        s += u'\nMeasurement Header\n'
        s += u'==================\n'
        s += u'    Aggregate CPU Use: {}\n'.format(self.aggregate_cpu_usage)
        s += u'    Concurrent Sessions: {}\n'.format(self.concurrent_sessions)
        s += u'    Configured Entities: {}\n'.format(self.configured_entities)
        s += u'    Mean Request Latency: {}\n'.format(
                                                     self.mean_request_latency)
        s += u'    Measurement Interval: {}\n'.format(
                                                     self.measurement_interval)
        s += u'    Measurement Fields Version: {}\n'.format(
                                               self.measurement_fields_version)
        s += u'    Memory Configured: {}\n'.format(self.memory_configured)
        s += u'    Memory Used: {}\n'.format(self.memory_used)
        s += u'    Media Ports in Use: {}\n'.format(self.media_ports_in_use)
        s += u'    Request Rate: {}\n'.format(self.request_rate)
        s += u'    Scaling mobile_flow_event: {}\n'.format(self.scaling_metric)
        for grp in self.additional_measurement_groups:
            s += u' Additional Measurement Grp: {}:\n'.format(grp['name'])
            for group in grp['fields']:
                s += u'    {}: {}\n'.format(group['name'], group['value'])
        for codec in self.codecs_in_use:
            s += u'    Codec Use: {} = {}\n'.format(codec[0], codec[1])
        for cpu in self.cpu_use:
            s += u'    CPU Use: {} = {}\n'.format(cpu[0], cpu[1])
        for feature in self.features_in_use:
            s += u'    Feature Use: {} = {}\n'.format(feature[0], feature[1])
        offset = ' ' * 29
        for fs in self.file_system_use:
            s += u'    File System Use: {}\n'.format(fs['identifier'])
            s += u'{}{} GB Block Storage Configured\n'.format(
                                                        offset,
                                                        fs['block_configured'])
            s += u'{}{} GB Block Storage Used\n'.format(offset,
                                                              fs['block_used'])
            s += u'{}{} Block Storage IOPS\n'.format(offset, fs['block_iops'])
            s += u'{}{} GB Ephemeral Storage Configured\n'.format(
                                                    offset,
                                                    fs['ephemeral_configured'])
            s += u'{}{} GB Ephemeral Storage Used\n'.format(
                                                          offset,
                                                          fs['ephemeral_iops'])
            s += u'{}{} Ephemeral Storage IOPS\n'.format(offset,
                                                         fs['ephemeral_iops'])
        for latency in self.latency_distribution:
            s += u'             Latency Bucket: {} - {} = {}\n'.format(
                                                           latency['low_end'],
                                                           latency['high_end'],
                                                           latency['count'])
        for vnic in self.vnic_use:
            s += u'    Virtual NIC Use: {}\n'.format(vnic['identifier'])
            s += u'{}{} Total Bytes In\n'.format(offset, vnic['bytes_in'])
            s += u'{}{} Total Bytes Out\n'.format(offset, vnic['bytes_out'])
            s += u'{}{} Broadcast Pkts In\n'.format(
                                                  offset,
                                                  vnic['broadcast_packets_in'])
            s += u'{}{} Broadcast Pkts Out\n'.format(
                                                 offset,
                                                 vnic['broadcast_packets_out'])
            s += u'{}{} Multicast Pkts In\n'.format(
                                                  offset,
                                                  vnic['multicast_packets_in'])
            s += u'{}{} Multicast Pkts Out\n'.format(
                                                 offset,
                                                 vnic['multicast_packets_out'])
            s += u'{}{} Unicast Pkts In\n'.format(offset,
                                                  vnic['unicast_packets_in'])
            s += u'{}{} Unicast Pkts Out\n'.format(offset,
                                                   vnic['unicast_packets_out'])
        return s

    def __str__(self):
        return unicode(self).encode('utf-8')

class MeasurementJSONEncoder(EventJSONEncoder):
    '''Specialization of the JSONEncoder to encode Measurements.'''
    def default(self, obj):
        '''
        Encode the supplied object, first checking it really is an Measurement.

        Any error handling is deferred to the base-class's handling.
        '''
        if isinstance(obj, Measurement):
            #------------------------------------------------------------------
            # Convert the Measurement into a dictionary which matches the JSON object
            # that definition in the Vendor Event Listener API specification.
            #------------------------------------------------------------------
            vel_dict = EventJSONEncoder.default(self, obj)
            meas_dict = {}

            #------------------------------------------------------------------
            # required fields
            #------------------------------------------------------------------
            meas_dict['concurrentSessions'] = obj.concurrent_sessions
            meas_dict['configuredEntities'] = obj.configured_entities
            meas_dict['cpuUsageArray'] = [{
                      'cpuIdentifier': cpu[0],
                      'percentUsage': cpu[1]
                      } for cpu in obj.cpu_use]
            meas_dict['filesystemUsageArray'] = [{
                          'blockConfigured': fs['block_configured'],
                          'blockIops': fs['block_iops'],
                          'blockUsed': fs['block_used'],
                          'ephemeralConfigured': fs['ephemeral_configured'],
                          'ephemeralIops': fs['ephemeral_iops'],
                          'ephemeralUsed': fs['ephemeral_used'],
                          'vmIdentifier': fs['identifier'],
                           } for fs in obj.file_system_use]
            meas_dict['latencyDistribution'] = [{
                          'countsInTheBucket': latency['count'],
                          'highEndOfLatencyBucket': latency['high_end'],
                          'lowEndOfLatencyBucket': latency['low_end'],
                           } for latency in obj.latency_distribution]
            meas_dict['meanRequestLatency'] = obj.mean_request_latency
            meas_dict['measurementInterval'] = obj.measurement_interval
            meas_dict['memoryConfigured'] = obj.memory_configured
            meas_dict['memoryUsed'] = obj.memory_used
            meas_dict['requestRate'] = obj.request_rate
            meas_dict['vNicUsageArray'] = [{
                       'broadcastPacketsIn': vnic['broadcast_packets_in'],
                       'broadcastPacketsOut': vnic['broadcast_packets_out'],
                       'bytesIn': vnic['bytes_in'],
                       'bytesOut': vnic['bytes_out'],
                       'multicastPacketsIn': vnic['multicast_packets_in'],
                       'multicastPacketsOut': vnic['multicast_packets_out'],
                       'unicastPacketsIn': vnic['unicast_packets_in'],
                       'unicastPacketsOut': vnic['unicast_packets_out'],
                       'vNicIdentifier': vnic['identifier'],
                       } for vnic in obj.vnic_use]

            #------------------------------------------------------------------
            # optional fields
            #------------------------------------------------------------------
            if len(obj.additional_measurement_groups) > 0:
                meas_dict['additionalMeasurements'] = [{
                          'name': measurementGroup['name'],
                          'measurements':[{
                            'name': field['name'],
                            'value': field['value'],
                            }for field in measurementGroup['fields']]
                        } for measurementGroup in obj.additional_measurement_groups]
            if len(obj.codecs_in_use) > 0:
                meas_dict['codecUsageArray'] = [{
                         'codecIdentifier': codec[0],
                         'codecUtilization': codec[1]
                         } for codec in obj.codecs_in_use]
            if obj.aggregate_cpu_usage:
                meas_dict['aggregateCpuUsage'] = obj.aggregate_cpu_usage
            meas_dict['measurementFieldsVersion'] = obj.measurement_fields_version
            if obj.media_ports_in_use:
                meas_dict['numberOfMediaPortsInUse'] = obj.media_ports_in_use
            if obj.scaling_metric:
                meas_dict['vnfcScalingMetric'] = obj.scaling_metric
            if len(obj.features_in_use) > 0:
                meas_dict['featureUsageArray'] = [{
                          'featureIdentifier': feature[0],
                          'featureUtilization': feature[1]
                          } for feature in obj.features_in_use]

            vel_dict['event']['measurementsForVfScalingFields'] = meas_dict
            logger.info('measurement encoded as: {}'.format(vel_dict))
            return vel_dict

        #----------------------------------------------------------------------
        # The object isn't of the expected type - it let the base encoder do
        # the work of raising the exception.
        #----------------------------------------------------------------------
        logger.error('Measurement JSON encoder can\'t handle: {}'.format(obj))
        return json.JSONEncoder.default(self, obj)
