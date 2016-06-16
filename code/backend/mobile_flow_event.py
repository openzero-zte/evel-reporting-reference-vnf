#!/usr/bin/env python
'''
Class for Mobile Flow.

Encapsulates the Mobile Flow specific info specified in the API.

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

logger = logging.getLogger('backend.mf')

class MobileFlow(Event):
    '''
    Vendor Event Listener - MobileFlow class.

    This class wraps the functionality required of Mobile Flow events and
    broadly corresponds to the mobileFlow definition in the Vendor Event
    Listener API specification.
    '''
    def __init__(self, event_id, vm_id, vm_name, vf_status='Active'):
        '''
        Constructor of the Event.

        Initializes the Mobile Flow's state deriving the VM information from
        that passed in (typically by the EventManager) and passing that
        information to the Event class we're derived from. Most of the
        Measurement's properties are initialized to be empty and may then be
        set by the instantiator of the object.
        '''
        super(MobileFlow, self).__init__(event_id,
                                          vm_id,
                                          vm_name,
                                          vf_status='Active')

        self.domain = u'mobileFlow'

        #----------------------------------------------------------------------
        # Mobile Flow required fields
        #----------------------------------------------------------------------
        self.flow_direction = u'unknown'
        self.ip_protocol_type = u'unknown'
        self.ip_version = u'unknown'
        self.other_endpoint_ip_address = u'unknown'
        self.other_endpoint_port = 0
        self.reporting_endpoint_ip_addr = u'unknown'
        self.reporting_endpoint_port = 0

        #----------------------------------------------------------------------
        # Mobile Flow optional fields
        #----------------------------------------------------------------------
        self.application_type = None
        self.app_protocol_type = None
        self.app_protocol_version = None
        self.cid = None
        self.connection_type = None
        self.ecgi = None
        self.gtp_protocol_type = None
        self.gtp_version = None
        self.http_header = None
        self.imei = None
        self.imsi = None
        self.lac = None
        self.mcc = None
        self.mnc = None
        self.msisdn = None
        self.other_functional_role = None
        self.rac = None
        self.radio_access_technology = None
        self.sac = None
        self.sampling_algorithm = None
        self.tac = None
        self.tunnel_id = None
        self.vlan_id = None

        #----------------------------------------------------------------------
        # GTP Per Flow Metrics required fields
        #----------------------------------------------------------------------
        self.avg_bit_error_rate = 0
        self.avg_packet_delay_variation = 0
        self.avg_packet_latency = 0
        self.avg_receive_throughput = 0
        self.avg_transmit_throughput = 0
        self.flow_activation_epoch = 0
        self.flow_activation_microsec = 0
        self.flow_deactivation_epoch = 0
        self.flow_deactivation_microsec = 0
        self.flow_deactivation_time = u'unknown'
        self.flow_status = u'unknown'
        self.max_packet_delay_variation = 0
        self.num_activation_failures = 0
        self.num_bit_errors = 0
        self.num_bytes_received = 0
        self.num_bytes_transmitted = 0
        self.num_dropped_packets = 0
        self.num_L7_bytes_received = 0
        self.num_L7_bytes_transmitted = 0
        self.num_lost_packets = 0
        self.num_out_of_order_packets = 0
        self.num_packet_errors = 0
        self.num_packets_received_excl_retrans = 0
        self.num_packets_received_incl_retrans = 0
        self.num_packets_transmitted_incl_retrans = 0
        self.num_retries = 0
        self.num_timeouts = 0
        self.num_tunneled_L7_bytes_received = 0
        self.round_trip_time = 0
        self.time_to_first_byte = 0

        # GTP Per Flow Metrics optional fields
        self.dur_connection_failed_status = None
        self.dur_tunnel_failed_status = None
        self.flow_activated_by = None
        self.flow_activation_time = None
        self.flow_deactivated_by = None
        self.gtp_connection_status = None
        self.gtp_tunnel_status = None
        self.large_packet_rtt = None
        self.large_packet_threshold = None
        self.max_receive_bit_rate = None
        self.max_transmit_bit_rate = None
        self.num_gtp_echo_failures = None
        self.num_gtp_tunnel_errors = None
        self.num_http_errors = None
        self.ip_tos_count_list = []
        self.ip_tos_list = []
        self.tcp_flag_count_list = []
        self.tcp_flag_list = []
        self.mobile_qci_cos_count_list = []
        self.mobile_qci_cos_list = []

        return

    def encode_json(self):
        '''
        Encode the Fault as JSON.

        Returns a string with the encoded JSON.
        '''
        return json.dumps(self, cls=MobileFlowJSONEncoder)

    def __unicode__(self):
        '''Provide a human-readable dump of the Mobile Flow's state.'''
        s = super(MobileFlow, self).__unicode__()

        # Mobile Flow required fields
        s += u'\nMobile Flow Fields\n'
        s += u'==================\n'
        s += u'    Domain: {}\n'.format(self.domain)
        s += u'    Flow Direction: {}\n'.format(self.flow_direction)
        s += u'    IP Protocol Type: {}\n'.format(self.ip_protocol_type)
        s += u'    IP version: {}\n'.format(self.ip_version)
        s += u'    Other Endpoint IP Address: {}\n'.format(
                                                self.other_endpoint_ip_address)
        s += u'    Other Endpoint Port: {}\n'.format(self.other_endpoint_port)
        s += u'    Reporting Endpoint IP Address: {}\n'.format(
                                               self.reporting_endpoint_ip_addr)
        s += u'    Reporting Endpoint Port: {}\n'.format(
                                                  self.reporting_endpoint_port)

        # Mobile Flow optional fields
        s += u'    Application Type: {}\n'.format(self.application_type)
        s += u'    IP Protocol Type: {}\n'.format(self.app_protocol_type)
        s += u'    Application Protocol Version: {}\n'.format(
                                                     self.app_protocol_version)
        s += u'    CID: {}\n'.format(self.cid)
        s += u'    Connection Type: {}\n'.format(self.connection_type)
        s += u'    ECGI: {}\n'.format(self.ecgi)
        s += u'    GTP Protocol Type: {}\n'.format(self.gtp_protocol_type)
        s += u'    GTP Version: {}\n'.format(self.gtp_version)
        s += u'    HTTP Header: {}\n'.format(self.http_header)
        s += u'    IMEI: {}\n'.format(self.imei)
        s += u'    IMSI: {}\n'.format(self.imsi)
        s += u'    LAC: {}\n'.format(self.lac)
        s += u'    MCC: {}\n'.format(self.mcc)
        s += u'    MNC: {}\n'.format(self.mnc)
        s += u'    MSISDN: {}\n'.format(self.msisdn)
        s += u'    Other Functional Role: {}\n'.format(
                                                    self.other_functional_role)
        s += u'    RAC: {}\n'.format(self.rac)
        s += u'    Radio Access Technology: {}\n'.format(
                                                  self.radio_access_technology)
        s += u'    SAC: {}\n'.format(self.sac)
        s += u'    Self Sampling Algorithm: {}\n'.format(
                                                       self.sampling_algorithm)
        s += u'    TAC: {}\n'.format(self.tac)
        s += u'    Tunnel ID: {}\n'.format(self.tunnel_id)
        s += u'    VLAN ID: {}\n'.format(self.vlan_id)

        # Mobile Flow GTP Metrics required fields
        s += u'    Average Bit Error Rate: {}\n'.format(
                                                       self.avg_bit_error_rate)
        s += u'    Average Packet Delay Variation: {}\n'.format(
                                               self.avg_packet_delay_variation)
        s += u'    Average Packet Latency: {}\n'.format(
                                                       self.avg_packet_latency)
        s += u'    Average Receive Throughput: {}\n'.format(
                                                   self.avg_receive_throughput)
        s += u'    Average Transmit Throughput: {}\n'.format(
                                                  self.avg_transmit_throughput)
        s += u'    Flow Activation Epoch: {}\n'.format(
                                                    self.flow_activation_epoch)
        s += u'    Flow Activation Microsecond: {}\n'.format(
                                                 self.flow_activation_microsec)
        s += u'    Flow Deactivation Epoch: {}\n'.format(
                                                 self.flow_deactivation_epoch)
        s += u'    Flow Deactivation Microsecond: {}\n'.format(
                                               self.flow_deactivation_microsec)
        s += u'    Flow Deactivation Time: {}\n'.format(
                                                   self.flow_deactivation_time)
        s += u'    Flow Status: {}\n'.format(self.flow_status)
        s += u'    Max Packet Delay Variation: {}\n'.format(
                                               self.max_packet_delay_variation)
        s += u'    Number of Activation Failures: {}\n'.format(
                                                  self.num_activation_failures)
        s += u'    Number of Bit Errors: {}\n'.format(self.num_bit_errors)
        s += u'    Number of Bytes Received: {}\n'.format(
                                                       self.num_bytes_received)
        s += u'    Number of Bytes  Transmitted: {}\n'.format(
                                                    self.num_bytes_transmitted)
        s += u'    Number of Dropped Packets: {}\n'.format(
                                                       self.num_dropped_packets)
        s += u'    Number of L7 Bytes Received: {}\n'.format(
                                                    self.num_L7_bytes_received)
        s += u'    Number of L7 Bytes Transmitted: {}\n'.format(
                                                 self.num_L7_bytes_transmitted)
        s += u'    Number of Lost Packets: {}\n'.format(self.num_lost_packets)
        s += u'    Number of Out of Order Packets: {}\n'.format(
                                                 self.num_out_of_order_packets)
        s += u'    Number of Packet Errors {}\n'.format(self.num_packet_errors)
        s += u'    Number of Packets Rx\'d excl retransmitted: {}\n'.format(
                                        self.num_packets_received_excl_retrans)
        s += u'    Number of Packets Rx\'d incl retransmitted: {}\n'.format(
                                        self.num_packets_received_incl_retrans)
        s += u'    Number of Packets Tx\'d incl retransmitted: {}\n'.format(
                                     self.num_packets_transmitted_incl_retrans)
        s += u'    Number of Retries: {}\n'.format(self.num_retries)
        s += u'    Number of Timeouts: {}\n'.format(self.num_timeouts)
        s += u'    Number of Tunnelled L7 Bytes Received: {}\n'.format(
                                           self.num_tunneled_L7_bytes_received)
        s += u'    Round Trip Time: {}\n'.format(self.round_trip_time)
        s += u'    Time to First Byte: {}\n'.format(self.time_to_first_byte)

        # Mobile Flow GTP Metrics Optional Fields
        s += u'    Duration - Connection Failed Status: {}\n'.format(
                                             self.dur_connection_failed_status)
        s += u'    Duration - Tunnel Failed Status: {}\n'.format(
                                                 self.dur_tunnel_failed_status)
        s += u'    Flow Activated By: {}\n'.format(self.flow_activated_by)
        s += u'    Flow Activated Time: {}\n'.format(self.flow_activation_time)
        s += u'    Flow Deactivated By: {}\n'.format(self.flow_deactivated_by)
        s += u'    GTP Connection Status: {}\n'.format(
                                                    self.gtp_connection_status)
        s += u'    GTP Tunnel Status: {}\n'.format(self.gtp_tunnel_status)
        s += u'    Large Packet Round Trip Time {}\n'.format(
                                                         self.large_packet_rtt)
        s += u'    Large Packet Threshold: {}\n'.format(
                                                   self.large_packet_threshold)
        s += u'    Max Receive Bit Rate: {}\n'.format(
                                                     self.max_receive_bit_rate)
        s += u'    Max Transmit Bit Rate: {}\n'.format(
                                                    self.max_transmit_bit_rate)
        s += u'    Number of GTP Echo Failures: {}\n'.format(
                                                    self.num_gtp_echo_failures)
        s += u'    Number of GTP Tunnel Failures: {}\n'.format(
                                                    self.num_gtp_tunnel_errors)
        s += u'    Number of HTTP Errors: {}\n'.format(self.num_http_errors)

        for tos in self.ip_tos_list:
            s += u'    TOS: {}\n'.format(tos)
        for tos_count in self.ip_tos_count_list:
            s += u'    TOS Count: {} = {}\n'.format(tos_count[0],
                                                    tos_count[1])
        for flag in self.tcp_flag_list:
            s += u'    TCP Flag: {}\n'.format(flag)
        for flag_count in self.tcp_flag_count_list:
            s += u'    TCP Flag Count: {} = {}\n'.format(flag_count[0],
                                                         flag_count[1])

        for cos in self.mobile_qci_cos_list:
            s += u'    Mobile QCI Cos: {}\n'.format(cos)
        for cos_count in self.mobile_qci_cos_count_list:
            s += u'    Mobile QCI COS Count: {} = {}\n'.format(cos_count[0],
                                                               cos_count[1])

        return s

    def __str__(self):
        return unicode(self).encode('utf-8')

class MobileFlowJSONEncoder(EventJSONEncoder):
    '''Specialisation of the JSONEncoder to encode Mobile Flow.'''
    def default(self, obj):
        '''
        Encode the supplied object, first checking it really is an Fault.

        Any error handling is deferred to the base-class's handling.
        '''
        if isinstance(obj, MobileFlow):
            #------------------------------------------------------------------
            # Convert the Measurement into a dictionary which matches the JSON
            # object definition in the Vendor Event Listener API specification.
            #------------------------------------------------------------------
            vel_dict = EventJSONEncoder.default(self, obj)
            mobile_flow_dict = {}

            # mobile flow required fields
            mobile_flow_dict['flowDirection'] = obj.flow_direction
            mobile_flow_dict['ipProtocolType'] = obj.ip_protocol_type
            mobile_flow_dict['ipVersion'] = obj.ip_version
            mobile_flow_dict[
                      'otherEndpointIpAddress'] = obj.other_endpoint_ip_address
            mobile_flow_dict['otherEndpointPort'] = obj.other_endpoint_port
            mobile_flow_dict[
                    'reportingEndpointIpAddr'] = obj.reporting_endpoint_ip_addr
            mobile_flow_dict[
                         'reportingEndpointPort'] = obj.reporting_endpoint_port

            # mobile flow optional fields
            if obj.application_type:
                mobile_flow_dict['applicationType'] = obj.application_type
            if obj.app_protocol_type:
                mobile_flow_dict['appProtocolType'] = obj.app_protocol_type
            if obj.app_protocol_version:
                mobile_flow_dict[
                               'appProtocolVersion'] = obj.app_protocol_version
            if obj.cid:
                mobile_flow_dict['cid'] = obj.cid
            if obj.connection_type:
                mobile_flow_dict['connectionType'] = obj.connection_type
            if obj.ecgi:
                mobile_flow_dict['ecgi'] = obj.ecgi
            if obj.gtp_protocol_type:
                mobile_flow_dict['gtpProtocolType'] = obj.gtp_protocol_type
            if obj.gtp_version:
                mobile_flow_dict['gtpVersion'] = obj.gtp_version
            if obj.http_header:
                mobile_flow_dict['httpHeader'] = obj.http_header
            if obj.imei:
                mobile_flow_dict['imei'] = obj.imei
            if obj.imsi:
                mobile_flow_dict['imsi'] = obj.imsi
            if obj.imsi:
                mobile_flow_dict['lac'] = obj.imsi
            if obj.mcc:
                mobile_flow_dict['mcc'] = obj.mcc
            if obj.mnc:
                mobile_flow_dict['mnc'] = obj.mnc
            if obj.msisdn:
                mobile_flow_dict['msisdn'] = obj.msisdn
            if obj.other_functional_role:
                mobile_flow_dict[
                              'otherFunctionaRole'] = obj.other_functional_role
            if obj.rac:
                mobile_flow_dict['rac'] = obj.rac
            if obj.radio_access_technology:
                mobile_flow_dict[
                         'radioAccessTechnology'] = obj.radio_access_technology
            if obj.sac:
                mobile_flow_dict['sac'] = obj.sac
            if obj.sampling_algorithm:
                mobile_flow_dict['samplingAlgorithm'] = obj.sampling_algorithm
            if obj.tac:
                mobile_flow_dict['tac'] = obj.tac
            if obj.tunnel_id:
                mobile_flow_dict['tunnelId'] = obj.tunnel_id
            if obj.vlan_id:
                mobile_flow_dict['vlanId'] = obj.vlan_id

            # GTP per flow metrics required fields
            mobile_flow_dict['gtpPerFlowMetrics'] = {
                'avgBitErrorRate': obj.avg_bit_error_rate,
                'avgBitErrorRate': obj.avg_bit_error_rate,
                'avgPacketDelayVariation': obj.avg_packet_delay_variation,
                'avgPacketLatency': obj.avg_packet_latency,
                'avgReceiveThroughput': obj.avg_receive_throughput,
                'avgTransmitThroughput': obj.avg_transmit_throughput,
                'flowActivationEpoch': obj.flow_activation_epoch,
                'flowActivationMicrosec': obj.flow_activation_microsec,
                'flowDeactivationEpoch': obj.flow_deactivation_epoch,
                'flowDeactivationMicrosec': obj.flow_deactivation_microsec,
                'flowDeactivationTime': obj.flow_deactivation_time,
                'flowStatus': obj.flow_status,
                'maxPacketDelayVariation': obj.max_packet_delay_variation,
                'numActivationFailures': obj.num_activation_failures,
                'numBitErrors': obj.num_bit_errors,
                'numBytesReceived': obj.num_bytes_received,
                'numBytesTransmitted': obj.num_bytes_transmitted,
                'numDroppedPackets': obj.num_dropped_packets,
                'numL7BytesReceived': obj.num_L7_bytes_received,
                'numL7BytesTransmitted': obj.num_L7_bytes_transmitted,
                'numLostPackets': obj.num_lost_packets,
                'numOutOfOrderPackets': obj.num_out_of_order_packets,
                'numPacketErrors': obj.num_packet_errors,
                'numPacketsReceivedExclRetrans':
                                         obj.num_packets_received_excl_retrans,
                'numPacketsReceivedInclRetrans':
                                         obj.num_packets_received_incl_retrans,
                'numPacketsTransmittedInclRetrans':
                                      obj.num_packets_transmitted_incl_retrans,
                'numRetries': obj.num_retries,
                'numTimeouts': obj.num_timeouts,
                'numTunneledL7BytesReceived':
                                            obj.num_tunneled_L7_bytes_received,
                'roundTripTime': obj.round_trip_time,
                'timeToFirstByte': obj.time_to_first_byte,
            }

            #------------------------------------------------------------------
            # optional fields are added outside of the main dictionary
            # definition as we can't put conditions in there
            #------------------------------------------------------------------
            if obj.dur_connection_failed_status:
                mobile_flow_dict[
                    'gtpPerFlowMetrics']['durConnectionFailedStatus'] = \
                                               obj.dur_connection_failed_status
            if obj.dur_tunnel_failed_status:
                mobile_flow_dict[
                    'gtpPerFlowMetrics']['durTunnelFailedStatus'] = \
                                                   obj.dur_tunnel_failed_status
            if obj.flow_activated_by:
                mobile_flow_dict['gtpPerFlowMetrics']['flowActivatedBy'] = \
                                                          obj.flow_activated_by
            if obj.flow_activation_time:
                mobile_flow_dict['gtpPerFlowMetrics']['flowActivationTime'] = \
                                                      obj.flow_activation_time
            if obj.flow_deactivated_by:
                mobile_flow_dict['gtpPerFlowMetrics']['flowDeactivatedBy'] = \
                                                        obj.flow_deactivated_by
            if obj.gtp_connection_status:
                mobile_flow_dict[
                    'gtpPerFlowMetrics']['gtpConnectionStatus'] = \
                                                      obj.gtp_connection_status
            if obj.gtp_tunnel_status:
                mobile_flow_dict['gtpPerFlowMetrics']['gtpunnelStatus'] = \
                                                          obj.gtp_tunnel_status
            if obj.large_packet_rtt:
                mobile_flow_dict['gtpPerFlowMetrics']['largePacketRtt'] = \
                                                           obj.large_packet_rtt
            if obj.large_packet_threshold:
                mobile_flow_dict[
                    'gtpPerFlowMetrics']['largePacketThreshold'] = \
                                                     obj.large_packet_threshold
            if obj.max_receive_bit_rate:
                mobile_flow_dict['gtpPerFlowMetrics']['maxReceiveBitRate'] = \
                                                       obj.max_receive_bit_rate
            if obj.max_transmit_bit_rate:
                mobile_flow_dict['gtpPerFlowMetrics']['maxTransmitBitRate'] = \
                                                      obj.max_transmit_bit_rate
            if obj.num_gtp_echo_failures:
                mobile_flow_dict['gtpPerFlowMetrics']['numGtpEchoFailures'] = \
                                                      obj.num_gtp_echo_failures
            if obj.num_gtp_tunnel_errors:
                mobile_flow_dict['gtpPerFlowMetrics']['numGtpTunnelErrors'] = \
                                                      obj.num_gtp_tunnel_errors
            if obj.num_http_errors:
                mobile_flow_dict['gtpPerFlowMetrics']['numHttpErrors'] = \
                                                            obj.num_http_errors

            if len(obj.ip_tos_count_list) > 0:
                mobile_flow_dict['gtpPerFlowMetrics']['ipTosCountList'] = [[
                                      str(tos_count_list[0]),
                                      tos_count_list[1]
                         ] for tos_count_list in obj.ip_tos_count_list]

            if len(obj.tcp_flag_count_list) > 0:
                mobile_flow_dict['gtpPerFlowMetrics']['tcpFlagCountList'] = [[
                                    flag_count_list[0],
                                    flag_count_list[1]
                         ] for flag_count_list in obj.tcp_flag_count_list]

            if len(obj.mobile_qci_cos_count_list) > 0:
                mobile_flow_dict[
                    'gtpPerFlowMetrics']['mobileQciCosCountList'] = [[
                                      cos_count_list[0],
                                      cos_count_list[1]
                         ] for cos_count_list in obj.mobile_qci_cos_count_list]

            if len(obj.ip_tos_list) > 0:
                mobile_flow_dict['gtpPerFlowMetrics']['ipTosList'] = \
                                               [tos for tos in obj.ip_tos_list]
            if len(obj.tcp_flag_list) > 0:
                mobile_flow_dict['gtpPerFlowMetrics']['tcpFlagList'] = \
                                           [flag for flag in obj.tcp_flag_list]
            if len(obj.mobile_qci_cos_list) > 0:
                mobile_flow_dict['gtpPerFlowMetrics']['mobileQciCosList'] = \
                                       [cos for cos in obj.mobile_qci_cos_list]

            #------------------------------------------------------------------
            # Assign and return the dictionary
            #------------------------------------------------------------------
            vel_dict['event']['mobileFlowFields'] = mobile_flow_dict
            logger.info('Mobile Flow encoded as: {}'.format(vel_dict))
            return vel_dict

        #----------------------------------------------------------------------
        # The object isn't of the expected type - it let the base encoder do
        # the work of raising the exception.
        #----------------------------------------------------------------------
        logger.error('Mobile Flow JSON encoder can\'t handle: {}'.format(obj))
        return json.JSONEncoder.default(self, obj)
