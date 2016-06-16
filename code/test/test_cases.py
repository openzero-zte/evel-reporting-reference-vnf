#!/usr/bin/env python
'''
Test framework for AT&T's Vendor Event Listener Reference VNF.

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

from system_test import SystemTestCase
from fault_event import Fault


class TestCases(SystemTestCase):

    def test_01_01_startup_heartbeat(self):
        '''Basic start-up/shutdown sequencing
        '''
        self.wait_stable()
        self.stop_child_processes()
        self.read_logs()
        self.assert_normal_logs()
        self.assert_good_responses(1)
        return

    def test_02_01_single_fault(self):
        '''Raise a single fault
        '''
        command = {'action': 'raise_fault',
                   'fault': {
                             'alarm_condition': 'Test Alarm Condition',
                             'event_type': 'Fault',
                             'severity': Fault.SEVERITY_MAJOR,
                             'specific_problem': 'Test problem',
                             'alarm_a_interface': 'Test Interface',
                             'additional_info': [['addinfo1', 'value1'],
                                                 ['addinfo2', 'value2']]
                             },
                   'vnf_overrides': {
                             'function_role': '',
                             'reporting_entity_id': '',
                             'reporting_entity_name': '',
                             'source_id': '',
                             'source_name': ''},
                   'fault_count': 1,
                   'fault_rate': 0,
                    }
        self.send_command(command)
        self.wait_stable()

        self.stop_child_processes()
        self.read_logs()
        self.assert_normal_logs()
        self.assert_good_responses(2)

        return

    def test_02_02_multiple_faults(self):
        '''Raise a multiple fault
        '''
        command = {'action': 'raise_fault',
                   'fault': {
                             'alarm_condition': 'Test Alarm Condition',
                             'event_type': 'Fault',
                             'severity': Fault.SEVERITY_MAJOR,
                             'specific_problem': 'Test problem',
                             'alarm_a_interface': 'Test Interface',
                             'additional_info': [['addinfo1', 'value1'],
                                                 ['addinfo2', 'value2']]
                             },
                   'vnf_overrides': {
                             'function_role': '',
                             'reporting_entity_id': '',
                             'reporting_entity_name': '',
                             'source_id': '',
                             'source_name': ''},
                   'fault_count': 10,
                   'fault_rate': 10,
                    }
        self.send_command(command)
        self.wait_stable(1)

        self.stop_child_processes()
        self.read_logs()
        self.assert_normal_logs()
        self.assert_good_responses(11)

        return

    def test_02_03_single_fault_override(self):
        '''Raise a single fault
        '''
        command = {'action': 'raise_fault',
                   'fault': {
                             'alarm_condition': 'Test Alarm Condition',
                             'event_type': 'Fault',
                             'severity': Fault.SEVERITY_MAJOR,
                             'specific_problem': 'Test problem',
                             'alarm_a_interface': 'Test Interface',
                             'additional_info': [['addinfo1', 'value1'],
                                                 ['addinfo2', 'value2']]
                             },
                   'vnf_overrides': {
                             'function_role': 'a',
                             'reporting_entity_id': 'b',
                             'reporting_entity_name': 'c',
                             'source_id': 'd',
                             'source_name': 'e'},
                   'fault_count': 1,
                   'fault_rate': 0,
                    }
        self.send_command(command)
        self.wait_stable()

        self.stop_child_processes()
        self.read_logs()
        self.assert_normal_logs()
        self.assert_good_responses(2)

        return

    def test_03_01_single_measurement(self):
        '''Raise a single measurement
        '''
        command = {'action': 'raise_measurement',
                   'measurement': {
                             'aggregate_cpu_usage': 1,
                             'concurrent_sessions': 2,
                             'configured_entities': 3,
                             'mean_request_latency': 4,
                             'measurement_interval': 5,
                             'memory_configured': 6,
                             'memory_used': 7,
                             'media_ports_in_use': 8,
                             'request_rate': 9,
                             'scaling_metric': 10,
                             'additional_measurement_groups': [
                                    {"fields": [
                                         {"name": "name1", "value": "value1"},
                                         {"name": "name1", "value": "value2"},
                                         {"name": "name3", "value": "value3"},
                                         {"name": "name4", "value": "value4"}],
                                    "name": "AddMeasureGroup1"}],
                             'codecs_in_use': [["codec1", 25], ["codec2", 35]],
                             'features_in_use': [["featureA", 35],
                                                 ["featureB", 45]],
                             'file_system_use': [{
                          "block_used": 45,
                          "ephemeral_configured": 55,
                          "block_configured": 25,
                          "ephemeral_iops": 65,
                          "ephemeral_used": 75,
                          "identifier": "c56a4180-65aa-42ec-a945-5fd210000000",
                          "block_iops": 35}],
                             'latency_distribution': [
                                     {"count": 15,
                                            "high_end": 45.0, "low_end": 25.0},
                                     {"count": 25,
                                           "high_end": 65.0, "low_end": 45.0}],
                             'vnic_use': [{"unicast_packets_out": 40,
                                           "broadcast_packets_out": 10,
                                           "unicast_packets_in": 35,
                                           "bytes_in": 15,
                                           "multicast_packets_out": 30,
                                           "broadcast_packets_in": 5,
                                           "multicast_packets_in": 25,
                                           "bytes_out": 20,
                                           "identifier": "vnic1"},
                                          {"unicast_packets_out": 400,
                                           "broadcast_packets_out": 100,
                                           "unicast_packets_in": 350,
                                           "bytes_in": 150,
                                           "multicast_packets_out": 300,
                                           "broadcast_packets_in": 50,
                                           "multicast_packets_in": 250,
                                           "bytes_out": 200,
                                           "identifier": "vnic2"}],
                             'cpu_use': [["cpuA", 35],
                                         ["cpuB", 45]],
                             },
                   'vnf_overrides': {
                             'function_role': '',
                             'reporting_entity_id': '',
                             'reporting_entity_name': '',
                             'source_id': '',
                             'source_name': ''},
                   'measurement_count': 1,
                   'measurement_rate': 0,
                    }
        self.send_command(command)
        self.wait_stable()

        self.stop_child_processes()
        self.read_logs()
        self.assert_normal_logs()
        self.assert_good_responses(2)

        return

    def test_03_02_multiple_measurements(self):
        '''Raise a multiple measurements
        '''
        command = {'action': 'raise_measurement',
                   'measurement': {
                             'aggregate_cpu_usage': 1,
                             'concurrent_sessions': 2,
                             'configured_entities': 3,
                             'mean_request_latency': 4,
                             'measurement_interval': 5,
                             'memory_configured': 6,
                             'memory_used': 7,
                             'media_ports_in_use': 8,
                             'request_rate': 9,
                             'scaling_metric': 10,
                             'additional_measurement_groups': [
                                    {"fields": [
                                         {"name": "name1", "value": "value1"},
                                         {"name": "name1", "value": "value2"},
                                         {"name": "name3", "value": "value3"},
                                         {"name": "name4", "value": "value4"}],
                                    "name": "AddMeasureGroup1"}],
                             'codecs_in_use': [["codec1", 25], ["codec2", 35]],
                             'features_in_use': [["featureA", 35],
                                                 ["featureB", 45]],
                             'file_system_use': [{
                          "block_used": 45,
                          "ephemeral_configured": 55,
                          "block_configured": 25,
                          "ephemeral_iops": 65,
                          "ephemeral_used": 75,
                          "identifier": "c56a4180-65aa-42ec-a945-5fd210000000",
                          "block_iops": 35}],
                             'latency_distribution': [
                                     {"count": 15,
                                            "high_end": 45.0, "low_end": 25.0},
                                     {"count": 25,
                                           "high_end": 65.0, "low_end": 45.0}],
                             'vnic_use': [{"unicast_packets_out": 40,
                                           "broadcast_packets_out": 10,
                                           "unicast_packets_in": 35,
                                           "bytes_in": 15,
                                           "multicast_packets_out": 30,
                                           "broadcast_packets_in": 5,
                                           "multicast_packets_in": 25,
                                           "bytes_out": 20,
                                           "identifier": "vnic1"},
                                          {"unicast_packets_out": 400,
                                           "broadcast_packets_out": 100,
                                           "unicast_packets_in": 350,
                                           "bytes_in": 150,
                                           "multicast_packets_out": 300,
                                           "broadcast_packets_in": 50,
                                           "multicast_packets_in": 250,
                                           "bytes_out": 200,
                                           "identifier": "vnic2"}],
                             'cpu_use': [["cpuA", 35],
                                         ["cpuB", 45]],
                             },
                   'vnf_overrides': {
                             'function_role': '',
                             'reporting_entity_id': '',
                             'reporting_entity_name': '',
                             'source_id': '',
                             'source_name': ''},
                   'measurement_count': 10,
                   'measurement_rate': 10,
                    }
        self.send_command(command)
        self.wait_stable(1)

        self.stop_child_processes()
        self.read_logs()
        self.assert_normal_logs()
        self.assert_good_responses(11)

        return

    def test_03_03_single_measurement_override(self):
        '''Raise a single measurement
        '''
        command = {'action': 'raise_measurement',
                   'measurement': {
                             'aggregate_cpu_usage': 1,
                             'concurrent_sessions': 2,
                             'configured_entities': 3,
                             'mean_request_latency': 4,
                             'measurement_interval': 5,
                             'memory_configured': 6,
                             'memory_used': 7,
                             'media_ports_in_use': 8,
                             'request_rate': 9,
                             'scaling_metric': 10,
                             'additional_measurement_groups': [
                                    {"fields": [
                                         {"name": "name1", "value": "value1"},
                                         {"name": "name1", "value": "value2"},
                                         {"name": "name3", "value": "value3"},
                                         {"name": "name4", "value": "value4"}],
                                    "name": "AddMeasureGroup1"}],
                             'codecs_in_use': [["codec1", 25], ["codec2", 35]],
                             'features_in_use': [["featureA", 35],
                                                 ["featureB", 45]],
                             'file_system_use': [{
                          "block_used": 45,
                          "ephemeral_configured": 55,
                          "block_configured": 25,
                          "ephemeral_iops": 65,
                          "ephemeral_used": 75,
                          "identifier": "c56a4180-65aa-42ec-a945-5fd210000000",
                          "block_iops": 35}],
                             'latency_distribution': [
                                     {"count": 15,
                                            "high_end": 45.0, "low_end": 25.0},
                                     {"count": 25,
                                           "high_end": 65.0, "low_end": 45.0}],
                             'vnic_use': [{"unicast_packets_out": 40,
                                           "broadcast_packets_out": 10,
                                           "unicast_packets_in": 35,
                                           "bytes_in": 15,
                                           "multicast_packets_out": 30,
                                           "broadcast_packets_in": 5,
                                           "multicast_packets_in": 25,
                                           "bytes_out": 20,
                                           "identifier": "vnic1"},
                                          {"unicast_packets_out": 400,
                                           "broadcast_packets_out": 100,
                                           "unicast_packets_in": 350,
                                           "bytes_in": 150,
                                           "multicast_packets_out": 300,
                                           "broadcast_packets_in": 50,
                                           "multicast_packets_in": 250,
                                           "bytes_out": 200,
                                           "identifier": "vnic2"}],
                             'cpu_use': [["cpuA", 35],
                                         ["cpuB", 45]],
                             },
                   'vnf_overrides': {
                             'function_role': 'a',
                             'reporting_entity_id': 'b',
                             'reporting_entity_name': 'c',
                             'source_id': 'd',
                             'source_name': 'e'},
                   'measurement_count': 1,
                   'measurement_rate': 0,
                    }
        self.send_command(command)
        self.wait_stable()

        self.stop_child_processes()
        self.read_logs()
        self.assert_normal_logs()
        self.assert_good_responses(2)

        return

    def test_04_01_single_mobile_flow(self):
        '''Raise a single Mobile Flow
        '''
        command = {'action': 'raise_mobile_flow',
                   'mobile_flow' :
                       {
                        'flow_direction':'one',
                        'ip_protocol_type': 'two',
                        'ip_version': 'three',
                        'other_endpoint_ip_address':  'four',
                        'other_endpoint_port': 1,
                        'reporting_endpoint_ip_addr': 'five',
                        'reporting_endpoint_port': 2,
                        'application_type': 'twelve',
                        'app_protocol_type': 'fifteen',
                        'app_protocol_version': 'fourteen',
                        'cid': 'fifteen',
                        'connection_type': 'sixteen',
                        'ecgi': 'seventeen',
                        'gtp_protocol_type': 'eighteen',
                        'gtp_version': 'nineteen',
                        'http_header': 'twenty one',
                        'imei': 'twenty two',
                        'imsi': 'twenty three',
                        'lac': 'twenty four',
                        'mcc': 'twenty five',
                        'mnc': 'twenty six',
                        'msisdn': 'twenty seven',
                        'other_functional_role': 'twent eight',
                        'rac': 'twenty nine',
                        'radio_access_technology': 'thirty',
                        'sac': 'thirty one',
                        'sampling_algorithm': 49,
                        'tac': 'thirty two',
                        'tunnel_id': 'thirty three',
                        'vlan_id': 'thirty four',
                        # GTP Per Flow Metrics fields
                        'avg_bit_error_rate': 3,
                        'avg_packet_delay_variation': 4,
                        'avg_packet_latency': 5,
                        'avg_receive_throughput': 6,
                        'avg_transmit_throughput': 7,
                        'flow_activation_epoch': 8,
                        'flow_activation_microsec': 9,
                        'flow_deactivation_epoch': 10,
                        'flow_deactivation_microsec': 11,
                        'flow_deactivation_time': 'six',
                        'flow_status': 'seven',
                        'max_packet_delay_variation': 12,
                        'num_activation_failures': 13,
                        'num_bit_errors': 14,
                        'num_bytes_received': 15,
                        'num_bytes_transmitted': 16,
                        'num_dropped_packets': 17,
                        'num_L7_bytes_received': 18,
                        'num_L7_bytes_transmitted': 19,
                        'num_lost_packets': 20,
                        'num_out_of_order_packets': 21,
                        'num_packet_errors': 22,
                        'num_packets_received_excl_retrans': 23,
                        'num_packets_received_incl_retrans': 24,
                        'num_packets_transmitted_incl_retrans': 25,
                        'num_retries': 26,
                        'num_timeouts': 27,
                        'num_tunneled_L7_bytes_received': 28,
                        'round_trip_time': 29,
                        'time_to_first_byte': 30,
                        'flow_activation_time': 'thirty five',
                        'dur_connection_failed_status': 0.0,
                        'dur_tunnel_failed_status': 0.1,
                        'flow_activated_by': 'nine',
                        'flow_deactivated_by': 'eight',
                        'gtp_connection_status': 'ten',
                        'gtp_tunnel_status': 'eleven',
                        'large_packet_rtt': 32,
                        'large_packet_threshold': 33,
                        'max_receive_bit_rate': 44,
                        'max_transmit_bit_rate': 45,
                        'num_gtp_echo_failures': 46,
                        'num_gtp_tunnel_errors': 47,
                        'num_http_errors': 48,
                        'ip_tos_count_list': [['one', 1], ['two', 2]],
                        'tcp_flag_count_list': [],
                        'mobile_qci_cos_count_list': [],
                        'tcp_flag_list': ['testlist1', 'testlist2'],
                        'ip_tos_list': ['testlist3', 'testlist4'],
                        'mobile_qci_cos_list': ['testlist5', 'testlist6'],
                        },

                   'vnf_overrides': {
                             'function_role': '',
                             'reporting_entity_id': '',
                             'reporting_entity_name': '',
                             'source_id': '',
                             'source_name': ''},
                   'mobile_flow_count': 1,
                   'mobile_flow_rate': 0,
                    }
        self.send_command(command)
        self.wait_stable()

        self.stop_child_processes()
        self.read_logs()
        self.assert_normal_logs()
        self.assert_good_responses(2)

        return

    def test_04_02_multiple_mobile_flow(self):
        '''Raise multiple Mobile Flow events
        '''
        command = {'action': 'raise_mobile_flow',
                   'mobile_flow' :
                       {
                        'flow_direction':'one',
                        'ip_protocol_type': 'two',
                        'ip_version': 'three',
                        'other_endpoint_ip_address':  'four',
                        'other_endpoint_port': 1,
                        'reporting_endpoint_ip_addr': 'five',
                        'reporting_endpoint_port': 2,
                        'application_type': 'twelve',
                        'app_protocol_type': 'fifteen',
                        'app_protocol_version': 'fourteen',
                        'cid': 'fifteen',
                        'connection_type': 'sixteen',
                        'ecgi': 'seventeen',
                        'gtp_protocol_type': 'eighteen',
                        'gtp_version': 'nineteen',
                        'http_header': 'twenty one',
                        'imei': 'twenty two',
                        'imsi': 'twenty three',
                        'lac': 'twenty four',
                        'mcc': 'twenty five',
                        'mnc': 'twenty six',
                        'msisdn': 'twenty seven',
                        'other_functional_role': 'twent eight',
                        'rac': 'twenty nine',
                        'radio_access_technology': 'thirty',
                        'sac': 'thirty one',
                        'sampling_algorithm': 49,
                        'tac': 'thirty two',
                        'tunnel_id': 'thirty three',
                        'vlan_id': 'thirty four',
                        # GTP Per Flow Metrics fields
                        'avg_bit_error_rate': 3,
                        'avg_packet_delay_variation': 4,
                        'avg_packet_latency': 5,
                        'avg_receive_throughput': 6,
                        'avg_transmit_throughput': 7,
                        'flow_activation_epoch': 8,
                        'flow_activation_microsec': 9,
                        'flow_deactivation_epoch': 10,
                        'flow_deactivation_microsec': 11,
                        'flow_deactivation_time': 'six',
                        'flow_status': 'seven',
                        'max_packet_delay_variation': 12,
                        'num_activation_failures': 13,
                        'num_bit_errors': 14,
                        'num_bytes_received': 15,
                        'num_bytes_transmitted': 16,
                        'num_dropped_packets': 17,
                        'num_L7_bytes_received': 18,
                        'num_L7_bytes_transmitted': 19,
                        'num_lost_packets': 20,
                        'num_out_of_order_packets': 21,
                        'num_packet_errors': 22,
                        'num_packets_received_excl_retrans': 23,
                        'num_packets_received_incl_retrans': 24,
                        'num_packets_transmitted_incl_retrans': 25,
                        'num_retries': 26,
                        'num_timeouts': 27,
                        'num_tunneled_L7_bytes_received': 28,
                        'round_trip_time': 29,
                        'time_to_first_byte': 30,
                        'flow_activation_time': 'thirty five',
                        'dur_connection_failed_status': 0.0,
                        'dur_tunnel_failed_status': 0.1,
                        'flow_activated_by': 'nine',
                        'flow_deactivated_by': 'eight',
                        'gtp_connection_status': 'ten',
                        'gtp_tunnel_status': 'eleven',
                        'large_packet_rtt': 32,
                        'large_packet_threshold': 33,
                        'max_receive_bit_rate': 44,
                        'max_transmit_bit_rate': 45,
                        'num_gtp_echo_failures': 46,
                        'num_gtp_tunnel_errors': 47,
                        'num_http_errors': 48,
                        'ip_tos_count_list': [['one', 1], ['two', 2]],
                        'tcp_flag_count_list': [],
                        'mobile_qci_cos_count_list': [],
                        'tcp_flag_list': ['testlist1', 'testlist2'],
                        'ip_tos_list': ['testlist3', 'testlist4'],
                        'mobile_qci_cos_list': ['testlist5', 'testlist6'],
                        },
                   'vnf_overrides': {
                             'function_role': '',
                             'reporting_entity_id': '',
                             'reporting_entity_name': '',
                             'source_id': '',
                             'source_name': ''},
                   'mobile_flow_count': 10,
                   'mobile_flow_rate': 10,
                    }

        self.send_command(command)
        self.wait_stable(1)

        self.stop_child_processes()
        self.read_logs()
        self.assert_normal_logs()
        self.assert_good_responses(11)

        return

    def test_04_03_single_mobile_flow_override(self):
        '''Raise a single Mobile Flow
        '''
        command = {'action': 'raise_mobile_flow',
                   'mobile_flow' :
                       {
                        'flow_direction':'one',
                        'ip_protocol_type': 'two',
                        'ip_version': 'three',
                        'other_endpoint_ip_address':  'four',
                        'other_endpoint_port': 1,
                        'reporting_endpoint_ip_addr': 'five',
                        'reporting_endpoint_port': 2,
                        'application_type': 'twelve',
                        'app_protocol_type': 'fifteen',
                        'app_protocol_version': 'fourteen',
                        'cid': 'fifteen',
                        'connection_type': 'sixteen',
                        'ecgi': 'seventeen',
                        'gtp_protocol_type': 'eighteen',
                        'gtp_version': 'nineteen',
                        'http_header': 'twenty one',
                        'imei': 'twenty two',
                        'imsi': 'twenty three',
                        'lac': 'twenty four',
                        'mcc': 'twenty five',
                        'mnc': 'twenty six',
                        'msisdn': 'twenty seven',
                        'other_functional_role': 'twent eight',
                        'rac': 'twenty nine',
                        'radio_access_technology': 'thirty',
                        'sac': 'thirty one',
                        'sampling_algorithm': 49,
                        'tac': 'thirty two',
                        'tunnel_id': 'thirty three',
                        'vlan_id': 'thirty four',
                        # GTP Per Flow Metrics fields
                        'avg_bit_error_rate': 3,
                        'avg_packet_delay_variation': 4,
                        'avg_packet_latency': 5,
                        'avg_receive_throughput': 6,
                        'avg_transmit_throughput': 7,
                        'flow_activation_epoch': 8,
                        'flow_activation_microsec': 9,
                        'flow_deactivation_epoch': 10,
                        'flow_deactivation_microsec': 11,
                        'flow_deactivation_time': 'six',
                        'flow_status': 'seven',
                        'max_packet_delay_variation': 12,
                        'num_activation_failures': 13,
                        'num_bit_errors': 14,
                        'num_bytes_received': 15,
                        'num_bytes_transmitted': 16,
                        'num_dropped_packets': 17,
                        'num_L7_bytes_received': 18,
                        'num_L7_bytes_transmitted': 19,
                        'num_lost_packets': 20,
                        'num_out_of_order_packets': 21,
                        'num_packet_errors': 22,
                        'num_packets_received_excl_retrans': 23,
                        'num_packets_received_incl_retrans': 24,
                        'num_packets_transmitted_incl_retrans': 25,
                        'num_retries': 26,
                        'num_timeouts': 27,
                        'num_tunneled_L7_bytes_received': 28,
                        'round_trip_time': 29,
                        'time_to_first_byte': 30,
                        'flow_activation_time': 'thirty five',
                        'dur_connection_failed_status': 0.0,
                        'dur_tunnel_failed_status': 0.1,
                        'flow_activated_by': 'nine',
                        'flow_deactivated_by': 'eight',
                        'gtp_connection_status': 'ten',
                        'gtp_tunnel_status': 'eleven',
                        'large_packet_rtt': 32,
                        'large_packet_threshold': 33,
                        'max_receive_bit_rate': 44,
                        'max_transmit_bit_rate': 45,
                        'num_gtp_echo_failures': 46,
                        'num_gtp_tunnel_errors': 47,
                        'num_http_errors': 48,
                        'ip_tos_count_list': [['one', 1], ['two', 2]],
                        'tcp_flag_count_list': [],
                        'mobile_qci_cos_count_list': [],
                        'tcp_flag_list': ['testlist1', 'testlist2'],
                        'ip_tos_list': ['testlist3', 'testlist4'],
                        'mobile_qci_cos_list': ['testlist5', 'testlist6'],
                        },

                   'vnf_overrides': {
                             'function_role': 'a',
                             'reporting_entity_id': 'b',
                             'reporting_entity_name': 'c',
                             'source_id': 'd',
                             'source_name': 'e'},
                   'mobile_flow_count': 1,
                   'mobile_flow_rate': 0,
                    }
        self.send_command(command)
        self.wait_stable()

        self.stop_child_processes()
        self.read_logs()
        self.assert_normal_logs()
        self.assert_good_responses(2)

        return

    def test_05_01_single_syslog(self):
        '''Raise a single syslog
        '''
        command = {'action': 'raise_syslog',
                   'syslog': {
                             'event_source_host': 'eventsourcehost',
                             'syslog_facility': 5,
                             'syslog_fields_version': 15,
                             'syslog_msg': 'syslog message',
                             'syslog_proc': 'syslog proc',
                             'syslog_proc_id': 25,
                             'syslog_sdata': 'syslog sdata',
                             'syslog_tag': 'syslog tag',
                             'syslog_ver': 35,
                             },
                   'vnf_overrides': {
                             'function_role': '',
                             'reporting_entity_id': '',
                             'reporting_entity_name': '',
                             'source_id': '',
                             'source_name': ''},
                   'syslog_count': 1,
                   'syslog_rate': 0,
                    }

        self.send_command(command)
        self.wait_stable()

        self.stop_child_processes()
        self.read_logs()
        self.assert_normal_logs()
        self.assert_good_responses(2)

        return

    def test_05_02_multiple_syslog(self):
        '''Raise a single syslog
        '''
        command = {'action': 'raise_syslog',
                   'syslog': {
                             'event_source_host': 'eventsourcehost',
                             'syslog_facility': 5,
                             'syslog_fields_version': 15,
                             'syslog_msg': 'syslog message',
                             'syslog_proc': 'syslog proc',
                             'syslog_proc_id': 25,
                             'syslog_sdata': 'syslog sdata',
                             'syslog_tag': 'syslog tag',
                             'syslog_ver': 35,
                             },
                   'vnf_overrides': {
                             'function_role': '',
                             'reporting_entity_id': '',
                             'reporting_entity_name': '',
                             'source_id': '',
                             'source_name': ''},
                   'syslog_count': 10,
                   'syslog_rate': 10,
                    }

        self.send_command(command)
        self.wait_stable(1)

        self.stop_child_processes()
        self.read_logs()
        self.assert_normal_logs()
        self.assert_good_responses(11)

        return

    def test_05_03_single_syslog_override(self):
        '''Raise a single syslog
        '''
        command = {'action': 'raise_syslog',
                   'syslog': {
                             'event_source_host': 'eventsourcehost',
                             'syslog_facility': 5,
                             'syslog_fields_version': 15,
                             'syslog_msg': 'syslog message',
                             'syslog_proc': 'syslog proc',
                             'syslog_proc_id': 25,
                             'syslog_sdata': 'syslog sdata',
                             'syslog_tag': 'syslog tag',
                             'syslog_ver': 35,
                             },
                   'vnf_overrides': {
                             'function_role': 'a',
                             'reporting_entity_id': 'b',
                             'reporting_entity_name': 'c',
                             'source_id': 'd',
                             'source_name': 'e'},
                   'syslog_count': 1,
                   'syslog_rate': 0,
                    }

        self.send_command(command)
        self.wait_stable()

        self.stop_child_processes()
        self.read_logs()
        self.assert_normal_logs()
        self.assert_good_responses(2)

        return

