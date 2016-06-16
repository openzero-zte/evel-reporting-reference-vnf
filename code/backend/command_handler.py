#!/usr/bin/env python
'''
Server which listens on a socket for commands to execute.

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

from SocketServer import BaseRequestHandler, TCPServer
from threading import Thread
import logging
import json
import event_manager
import time

logger = logging.getLogger('backend.ch')

class CommandHandler(BaseRequestHandler):
    '''
    Command handler which wraps a TCP socket and dispatches the commands
    received.
    '''

    def setup(self):
        '''Prepare the CommandHandler for use.

        Identifies the Event Manager which will be used to send events.
        '''

        self.event_manager = event_manager.get_event_manager()
        logger.debug('Command handler Event Manager identified')

    def handle(self):
        '''
        Handle connections to the socket. Tasks get deferred to worker threads.
        '''

        logger.debug('Got connection from: {}'.format(self.client_address))
        while True:
            msg = self.request.recv(8192)
            if not msg:
                break
            logger.debug('Got msg: {}'.format(msg))
            try:
                msg_decoded = json.loads(msg)
                action = msg_decoded['action']
                if (action == 'raise_fault'):
                    logger.debug('Starting thread for deferred Faults')
                    task_thread = Thread(target=self.raise_faults,
                                         args=(msg_decoded['fault'],
                                               msg_decoded['vnf_overrides'],
                                               msg_decoded['fault_count'],
                                               msg_decoded['fault_rate']))
                    task_thread.daemon = True
                    task_thread.start()
                elif (action == 'raise_measurement'):
                    logger.debug('Starting thread for deferred Measurements')
                    task_thread = Thread(
                                     target=self.raise_measurements,
                                     args=(msg_decoded['measurement'],
                                           msg_decoded['vnf_overrides'],
                                           msg_decoded['measurement_count'],
                                           msg_decoded['measurement_rate']))
                    task_thread.daemon = True
                    task_thread.start()
                elif (action == 'raise_mobile_flow'):
                    logger.debug('Starting thread for deferred Metrics')
                    task_thread = Thread(
                                     target=self.raise_mobile_flow,
                                     args=(msg_decoded['mobile_flow'],
                                           msg_decoded['vnf_overrides'],
                                           msg_decoded['mobile_flow_count'],
                                           msg_decoded['mobile_flow_rate']))
                    task_thread.daemon = True
                    task_thread.start()
                elif (action == 'raise_syslog'):
                    logger.debug('Starting thread for syslog')
                    task_thread = Thread(
                                     target=self.raise_syslog,
                                     args=(msg_decoded['syslog'],
                                           msg_decoded['vnf_overrides'],
                                           msg_decoded['syslog_count'],
                                           msg_decoded['syslog_rate']))
                    task_thread.daemon = True
                    task_thread.start()
                elif (action == 'prepare_terminate'):
                    logger.debug('Initiate the preparations for termination')
                    self.event_manager.prepare_terminate(
                                                     msg_decoded['dwell_time'])
                elif (action == 'activate'):
                    logger.debug('Reset the VNF to be active')
                    self.event_manager.set_active()
                elif (action == 'ping'):
                    logger.debug('Received ping - no action necessary!')
                else:
                    logger.warning('Unrecognized action: {}'.format(action))

            except Exception as e:
                logger.error('Failed to decode command {}\n'
                             'Raised: {}'.format(msg, e))
                raise e
        return

    def raise_faults(self, fault, vnf_overrides, count=1, rate=0.1):
        '''
        This method is called from a worker thread to generate the specified
        *count* of *fault* at the specified *rate*.  The rate is specified in
        events/sec.
        '''
        try:
            #------------------------------------------------------------------
            # Extract the information of interest from the command.
            #------------------------------------------------------------------
            alarm_condition = fault['alarm_condition']
            event_type = fault['event_type']
            severity = fault['severity']
            specific_problem = fault['specific_problem']
            alarm_a_interface = fault['alarm_a_interface']
            additional_info = fault['additional_info']
            logger.info(u'Raising {} faults: {}\n'
                        u'             Event Type: {}\n'
                        u'               Severity: {}\n'
                        u'       Specific Problem: {}\n'
                        u'           Alarm A Int.: {}\n'
                        u'            Add\'l Info.: {}\n'
                        u'          VNF Overrides: {}\n'.format(
                                              count,
                                              alarm_condition,
                                              event_type,
                                              severity,
                                              specific_problem,
                                              alarm_a_interface,
                                              additional_info,
                                              vnf_overrides
                                              ))

            #------------------------------------------------------------------
            # Transcribe the fields from the command into a new fault and post
            # that fault to the manager.  If this fault is part of a set,
            # ensure that the sequence is set in range 1..n.
            #------------------------------------------------------------------
            for fault_num in range(count):
                logger.debug('Raising event {} of {}'.format(fault_num + 1,
                                                             count))
                flt = self.event_manager.new_fault()
                if (count > 1):
                    flt.sequence = fault_num + 1
                flt.alarm_condition = alarm_condition
                flt.event_type = event_type
                flt.event_severity = severity
                flt.specific_problem = specific_problem
                flt.alarm_a_interface = alarm_a_interface
                flt.alarm_additional_info = additional_info

                #--------------------------------------------------------------
                # The VNF environment fields may get overridden.  Update if
                # required.
                #--------------------------------------------------------------
                self.override_vnf_environment(flt, vnf_overrides)

                #--------------------------------------------------------------
                # Post the event and then sleep if necessary.
                #--------------------------------------------------------------
                self.event_manager.post_event(flt)
                if (rate > 0.0):
                    time.sleep(1.0 / rate)

            logger.debug('Sending {} faults done - thread terminating'.format(
                                                                        count))
        except Exception as e:
            logger.error('Fault thread exception {}\n'
                         'Raised: {}'.format(fault, e))
            raise e
        return

    def raise_measurements(self,
                           measurement,
                           vnf_overrides,
                           count=1,
                           rate=0.1):
        '''
        This method is called from a worker thread to generate the specified
        *count* of *measurement* at the specified *rate*.  The rate is
        specified in events/sec.

        Catch unexpected exceptions that cause the thread to fail.
        '''
        try:
            logger.info(u'Raising {} measurements: {}'.format(count,
                                                              measurement))

            #------------------------------------------------------------------
            # Extract the information of interest from the command.  If this
            # measurement is part of a set,  ensure that the sequence is set in
            # range 1..n.
            #------------------------------------------------------------------
            aggregate_cpu_usage = measurement['aggregate_cpu_usage']
            concurrent_sessions = measurement['concurrent_sessions']
            configured_entities = measurement['configured_entities']
            mean_request_latency = measurement['mean_request_latency']
            measurement_interval = measurement['measurement_interval']
            memory_configured = measurement['memory_configured']
            memory_used = measurement['memory_used']
            media_ports_in_use = measurement['media_ports_in_use']
            request_rate = measurement['request_rate']
            scaling_metric = measurement['scaling_metric']
            measurement_groups = measurement['additional_measurement_groups']
            codecs_in_use = measurement['codecs_in_use']
            features_in_use = measurement['features_in_use']
            file_system_use = measurement['file_system_use']
            latency_distribution = measurement['latency_distribution']
            vnic_use = measurement['vnic_use']
            cpu_use = measurement['cpu_use']

            #------------------------------------------------------------------
            # Transcribe the fields from the command into a new Measurement.
            #------------------------------------------------------------------
            for measurement_num in range(count):
                logger.debug('Raising event {} of {}'.format(
                                                         measurement_num + 1,
                                                         count))
                meas = self.event_manager.new_measurement()
                if (count > 1):
                    meas.sequence = measurement_num + 1
                meas.aggregate_cpu_usage = aggregate_cpu_usage
                meas.concurrent_sessions = concurrent_sessions
                meas.configured_entities = configured_entities
                meas.mean_request_latency = mean_request_latency
                meas.measurement_interval = measurement_interval
                meas.memory_configured = memory_configured
                meas.memory_used = memory_used
                meas.media_ports_in_use = media_ports_in_use
                meas.request_rate = request_rate
                meas.scaling_metric = scaling_metric
                meas.additional_measurement_groups = []
                for grp in measurement_groups:
                    new_grp = {}
                    new_grp['name'] = grp['name']
                    new_grp['fields'] = [m for m in grp['fields']
                                                 if (len(m['name']) > 0)]
                    meas.additional_measurement_groups.append(new_grp)

                meas.codecs_in_use = codecs_in_use
                meas.features_in_use = features_in_use
                meas.file_system_use = file_system_use
                meas.latency_distribution = latency_distribution
                meas.vnic_use = vnic_use
                meas.cpu_use = cpu_use

                #--------------------------------------------------------------
                # The VNF environment fields may get overridden.  Update if
                # required.
                #--------------------------------------------------------------
                self.override_vnf_environment(meas, vnf_overrides)

                #--------------------------------------------------------------
                # Now we have the Measurement, post the event to the manager so
                # that it can send to the Collector.  If we're doing multiple
                # events and we're not just trying to go as fast as possible,
                # sleep for duration to pace ourselves.
                #--------------------------------------------------------------
                self.event_manager.post_event(meas)
                if (count > 1 and rate > 0.0):
                    time.sleep(1.0 / rate)

            logger.debug('Sending {} measurements done.  '
                         'Thread exiting'.format(count))

        except Exception as e:
            logger.error('Measurement thread exception {}\n'
                         'Raised: {}'.format(measurement, e))
            raise e
        return

    def raise_mobile_flow(self, mobile_flow, vnf_overrides, count=1, rate=0.1):
        '''
        This method is called from a worker thread to generate the specified
        *count* of *mobile flow* at the specified *rate*.  The rate is
        specified in events/sec.

        Catch unexpected exceptions that cause the thread to fail.
        '''
        try:
            logger.info(u'Raising {} Mobile Flow: {}'.format(count,
                                                             mobile_flow))

            #------------------------------------------------------------------
            # Extract the information of interest from the command.
            #------------------------------------------------------------------
            avg_bit_error_rate = mobile_flow['avg_bit_error_rate']
            avg_packet_delay_variation = mobile_flow[
                                                  'avg_packet_delay_variation']
            avg_packet_latency = mobile_flow['avg_packet_latency']
            avg_receive_throughput = mobile_flow['avg_receive_throughput']
            avg_transmit_throughput = mobile_flow['avg_transmit_throughput']
            flow_activation_epoch = mobile_flow['flow_activation_epoch']
            flow_activation_microsec = mobile_flow['flow_activation_microsec']
            flow_activation_time = mobile_flow['flow_activation_time']
            flow_deactivation_epoch = mobile_flow['flow_deactivation_epoch']
            flow_deactivated_by = mobile_flow['flow_deactivated_by']
            flow_deactivation_microsec = mobile_flow[
                                                  'flow_deactivation_microsec']
            flow_deactivation_time = mobile_flow['flow_deactivation_time']
            flow_status = mobile_flow['flow_status']
            max_packet_delay_variation = mobile_flow[
                                                  'max_packet_delay_variation']
            num_activation_failures = mobile_flow['num_activation_failures']
            num_bit_errors = mobile_flow['num_bit_errors']
            num_bytes_received = mobile_flow['num_bytes_received']
            num_bytes_transmitted = mobile_flow['num_bytes_transmitted']
            num_dropped_packets = mobile_flow['num_dropped_packets']
            num_L7_bytes_received = mobile_flow['num_L7_bytes_received']
            num_L7_bytes_transmitted = mobile_flow['num_L7_bytes_transmitted']
            num_lost_packets = mobile_flow['num_lost_packets']
            num_out_of_order_packets = mobile_flow['num_out_of_order_packets']
            num_packet_errors = mobile_flow['num_packet_errors']
            num_packets_received_excl_retrans = mobile_flow[
                                           'num_packets_received_excl_retrans']
            num_packets_received_incl_retrans = mobile_flow[
                                           'num_packets_received_incl_retrans']
            num_packets_transmitted_incl_retrans = mobile_flow[
                                        'num_packets_transmitted_incl_retrans']
            num_retries = mobile_flow['num_retries']
            num_timeouts = mobile_flow['num_timeouts']
            num_tunneled_L7_bytes_received = mobile_flow[
                                              'num_tunneled_L7_bytes_received']
            large_packet_rtt = mobile_flow['large_packet_threshold']
            large_packet_threshold = mobile_flow['large_packet_threshold']
            round_trip_time = mobile_flow['round_trip_time']
            time_to_first_byte = mobile_flow['time_to_first_byte']
            num_http_errors = mobile_flow['num_http_errors']
            num_gtp_tunnel_errors = mobile_flow['num_gtp_tunnel_errors']
            num_gtp_echo_failures = mobile_flow['num_gtp_echo_failures']
            gtp_connection_status = mobile_flow['gtp_connection_status']
            flow_activated_by = mobile_flow['flow_activated_by']
            dur_connection_failed_status = mobile_flow[
                                                'dur_connection_failed_status']
            max_receive_bit_rate = mobile_flow['max_receive_bit_rate']
            max_transmit_bit_rate = mobile_flow['max_transmit_bit_rate']
            application_type = mobile_flow['application_type']
            app_protocol_type = mobile_flow['app_protocol_type']
            app_protocol_version = mobile_flow['app_protocol_version']
            cid = mobile_flow['cid']
            connection_type = mobile_flow['connection_type']
            ecgi = mobile_flow['ecgi']
            gtp_protocol_type = mobile_flow['gtp_protocol_type']
            gtp_version = mobile_flow['gtp_version']
            http_header = mobile_flow['http_header']
            imei = mobile_flow['imei']
            imsi = mobile_flow['imsi']
            lac = mobile_flow['lac']
            mcc = mobile_flow['mcc']
            mnc = mobile_flow['mnc']
            msisdn = mobile_flow['msisdn']
            other_functional_role = mobile_flow['other_functional_role']
            rac = mobile_flow['rac']
            radio_access_technology = mobile_flow['radio_access_technology']
            sac = mobile_flow['sac']
            sampling_algorithm = mobile_flow['sampling_algorithm']
            tac = mobile_flow['tac']
            tunnel_id = mobile_flow['tunnel_id']
            vlan_id = mobile_flow['vlan_id']
            dur_tunnel_failed_status = mobile_flow['dur_tunnel_failed_status']
            ip_tos_count_list = mobile_flow['ip_tos_count_list']
            ip_tos_list = mobile_flow['ip_tos_list']
            tcp_flag_count_list = mobile_flow['tcp_flag_count_list']
            tcp_flag_list = mobile_flow['tcp_flag_list']
            mobile_qci_cos_count_list = mobile_flow[
                                                   'mobile_qci_cos_count_list']
            mobile_qci_cos_list = mobile_flow['mobile_qci_cos_list']

            #------------------------------------------------------------------
            # Transcribe the fields from the command into a new MobileFlow.
            # If this event is part of a set,  ensure that the sequence is set
            # in range 1..n.
            #------------------------------------------------------------------
            for mobile_flow_num in range(count):
                logger.debug('Raising event {} of {}'.format(
                                                         mobile_flow_num + 1,
                                                         count))
                mobile_flow = self.event_manager.new_mobile_flow()
                if (count > 1):
                    mobile_flow.sequence = mobile_flow_num + 1
                mobile_flow.avg_bit_error_rate = avg_bit_error_rate
                mobile_flow.avg_packet_delay_variation = \
                                                     avg_packet_delay_variation
                mobile_flow.avg_packet_latency = avg_packet_latency
                mobile_flow.avg_receive_throughput = avg_receive_throughput
                mobile_flow.avg_transmit_throughput = avg_transmit_throughput
                mobile_flow.flow_activation_epoch = flow_activation_epoch
                mobile_flow.flow_activation_microsec = flow_activation_microsec
                mobile_flow.flow_activation_time = flow_activation_time
                mobile_flow.flow_deactivation_epoch = flow_deactivation_epoch
                mobile_flow.flow_deactivated_by = flow_deactivated_by
                mobile_flow.flow_deactivation_microsec = \
                                                     flow_deactivation_microsec
                mobile_flow.flow_deactivation_time = flow_deactivation_time
                mobile_flow.flow_status = flow_status
                mobile_flow.max_packet_delay_variation = \
                                                     max_packet_delay_variation
                mobile_flow.num_activation_failures = num_activation_failures
                mobile_flow.num_bit_errors = num_bit_errors
                mobile_flow.num_bytes_received = num_bytes_received
                mobile_flow.num_bytes_transmitted = num_bytes_transmitted
                mobile_flow.num_dropped_packets = num_dropped_packets
                mobile_flow.num_L7_bytes_received = num_L7_bytes_received
                mobile_flow.num_L7_bytes_transmitted = num_L7_bytes_transmitted
                mobile_flow.num_lost_packets = num_lost_packets
                mobile_flow.num_out_of_order_packets = num_out_of_order_packets
                mobile_flow.num_packet_errors = num_packet_errors
                mobile_flow.num_packets_received_excl_retrans = \
                                              num_packets_received_excl_retrans
                mobile_flow.num_packets_received_incl_retrans = \
                                              num_packets_received_incl_retrans
                mobile_flow.num_packets_transmitted_incl_retrans = \
                                           num_packets_transmitted_incl_retrans
                mobile_flow.num_retries = num_retries
                mobile_flow.num_timeouts = num_timeouts
                mobile_flow.num_tunneled_L7_bytes_received = \
                                                 num_tunneled_L7_bytes_received
                mobile_flow.large_packet_rtt = large_packet_rtt
                mobile_flow.large_packet_threshold = large_packet_threshold
                mobile_flow.round_trip_time = round_trip_time
                mobile_flow.time_to_first_byte = time_to_first_byte
                mobile_flow.num_http_errors = num_http_errors
                mobile_flow.num_gtp_tunnel_errors = num_gtp_tunnel_errors
                mobile_flow.num_gtp_echo_failures = num_gtp_echo_failures
                mobile_flow.gtp_connection_status = gtp_connection_status
                mobile_flow.dur_connection_failed_status = \
                                                   dur_connection_failed_status
                mobile_flow.flow_activated_by = flow_activated_by
                mobile_flow.max_receive_bit_rate = max_receive_bit_rate
                mobile_flow.application_type = application_type
                mobile_flow.app_protocol_type = app_protocol_type
                mobile_flow.app_protocol_version = app_protocol_version
                mobile_flow.cid = cid
                mobile_flow.connection_type = connection_type
                mobile_flow.ecgi = ecgi
                mobile_flow.gtp_protocol_type = gtp_protocol_type
                mobile_flow.gtp_version = gtp_version
                mobile_flow.http_header = http_header
                mobile_flow.max_transmit_bit_rate = max_transmit_bit_rate
                mobile_flow.imei = imei
                mobile_flow.imsi = imsi
                mobile_flow.lac = lac
                mobile_flow.mcc = mcc
                mobile_flow.mnc = mnc
                mobile_flow.msisdn = msisdn
                mobile_flow.other_functional_role = other_functional_role
                mobile_flow.rac = rac
                mobile_flow.radio_access_technology = radio_access_technology
                mobile_flow.sac = sac
                mobile_flow.sampling_algorithm = sampling_algorithm
                mobile_flow.tac = tac
                mobile_flow.tunnel_id = tunnel_id
                mobile_flow.vlan_id = vlan_id
                mobile_flow.dur_tunnel_failed_status = dur_tunnel_failed_status
                mobile_flow.ip_tos_count_list = ip_tos_count_list
                mobile_flow.ip_tos_list = ip_tos_list
                mobile_flow.tcp_flag_count_list = tcp_flag_count_list
                mobile_flow.tcp_flag_list = tcp_flag_list
                mobile_flow.mobile_qci_cos_count_list = \
                                                      mobile_qci_cos_count_list
                mobile_flow.mobile_qci_cos_list = mobile_qci_cos_list

                #--------------------------------------------------------------
                # The VNF environment fields may get overridden.  Update if
                # required.
                #--------------------------------------------------------------
                self.override_vnf_environment(mobile_flow, vnf_overrides)

                #--------------------------------------------------------------
                # Now we have the MobileFlow, post the event to the manager so
                # that it can send to the Collector.  If we're doing multiple
                # events and we're not just trying to go as fast as possible,
                # sleep for duration to pace ourselves.
                #--------------------------------------------------------------
                self.event_manager.post_event(mobile_flow)
                if (count > 1 and rate > 0.0):
                    time.sleep(1.0 / rate)

            logger.debug('Sending {} MobileFlow done.  '
                         'Thread exiting'.format(count))

        except Exception as e:
            logger.error('Mobile Flow thread exception {}\n'
                         'Raised: {}'.format(mobile_flow, e))
            raise e
        return

    def raise_syslog(self, syslog, vnf_overrides, count=1, rate=0.1):
        '''
        This method is called from a worker thread to generate the specified
        *count* of *syslog* at the specified *rate*.  The rate is specified in
        events/sec.
        '''
        try:
            #------------------------------------------------------------------
            # Extract the information of interest from the command.
            #------------------------------------------------------------------
            event_source_host = syslog['event_source_host']
            syslog_tag = syslog['syslog_tag']
            syslog_msg = syslog['syslog_msg']
            syslog_facility = syslog['syslog_facility']
            syslog_proc = syslog['syslog_proc']
            syslog_proc_id = syslog['syslog_proc_id']
            syslog_ver = syslog['syslog_ver']
            syslog_sdata = syslog['syslog_sdata']
            logger.info(u'Raising {} Syslogs:\n'
                        u'    Host: {}\n'
                        u'    Tag: {}\n'
                        u'    Facility: {}\n'
                        u'    Message: {}\n'
                        u'    Proc.: {}\n'
                        u'    Proc. ID: {}\n'
                        u'    Version.: {}\n'
                        u'    SData.: {}\n'.format(count,
                                                   event_source_host,
                                                   syslog_tag,
                                                   syslog_msg,
                                                   syslog_facility,
                                                   syslog_proc,
                                                   syslog_proc_id,
                                                   syslog_ver,
                                                   syslog_sdata))

            #------------------------------------------------------------------
            # Transcribe the fields from the command into a new fault and post
            # that fault to the manager.
            #
            # If this event is part of a set,  ensure that the sequence is set
            # in range 1..n.
            #------------------------------------------------------------------
            for syslog_num in range(count):
                logger.debug('Raising event {} of {}'.format(syslog_num + 1,
                                                             count))
                syslg = self.event_manager.new_syslog()
                if (count > 1):
                    syslg.sequence = syslog_num + 1
                syslg.syslog_tag = syslog_tag
                syslg.syslog_msg = syslog_msg

                syslg.event_source_host = event_source_host
                syslg.syslog_facility = syslog_facility
                syslg.syslog_proc = syslog_proc
                syslg.syslog_proc_id = syslog_proc_id
                syslg.syslog_ver = syslog_ver
                syslg.syslog_sdata = syslog_sdata

                #--------------------------------------------------------------
                # The VNF environment fields may get overridden.  Update if
                # required.
                #--------------------------------------------------------------
                self.override_vnf_environment(syslg, vnf_overrides)

                #--------------------------------------------------------------
                # Now we have the Syslog, post the event to the manager so
                # that it can send to the Collector.  If we're doing multiple
                # events and we're not just trying to go as fast as possible,
                # sleep for duration to pace ourselves.
                #--------------------------------------------------------------
                self.event_manager.post_event(syslg)
                if (rate > 0.0):
                    time.sleep(1.0 / rate)

            logger.debug('Sending {} Syslog done - thread terminating'
                                                                .format(count))
        except Exception as e:
            logger.error('Syslog thread exception {}\n'
                         'Raised: {}'.format(syslog, e))
            raise e
        return

    def override_vnf_environment(self, event, vnf_overrides):
        if (vnf_overrides['function_role']):
            event.functional_role = vnf_overrides['function_role']
        if (vnf_overrides['reporting_entity_id']):
            event.reporting_entity_id = vnf_overrides['reporting_entity_id']
        if (vnf_overrides['reporting_entity_name']):
            event.reporting_entity_name = vnf_overrides['reporting_entity_name']
        if (vnf_overrides['source_id']):
            event.source_id = vnf_overrides['source_id']
        if (vnf_overrides['source_name']):
            event.source_name = vnf_overrides['source_name']
        return

def start_server(port):
    '''Kick-off the server thread listening for connections on *port*.'''

    logger.info('Starting server on port {}...'.format(port))
    server_thread = Thread(target=server, args=(port,))
    server_thread.daemon = True
    server_thread.start()
    logger.debug('Server started')

def server(port):
    '''The server thread, listening for connections on *port*.'''
    logger.info('Server listening on {}...'.format(port))
    serv = TCPServer(('', port), CommandHandler)
    serv.serve_forever()
