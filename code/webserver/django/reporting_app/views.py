import socket
import json
import sys
import logging

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F

from .forms import FaultForm, MeasurementForm, LifecycleForm, MobileFlowForm
from .forms import SyslogForm
from models import Fault, Measurement, MobileFlow, Syslog
from models import EventCounter

from warnings import catch_warnings

logger = logging.getLogger(__name__)

banner = 'AT&T Vendor Event Listener Service - Reference VNF'

# Create your views here.

def base_redirect(request):
    return HttpResponseRedirect('/reporting')

def clear_event_counter(request):
    #--------------------------------------------------------------------------
    # If we end up in here, just clear the counter
    #--------------------------------------------------------------------------
    clear_events()
    return render(request, 'reporting_app/index.html', {'title': banner})

def raise_fault(request):
    if request.method == 'POST':

        #----------------------------------------------------------------------
        # If this is a POST request we need to process the form data
        # create a form instance and populate it with data from the request,
        # checking whether it's valid.
        #----------------------------------------------------------------------
        fault_form = FaultForm(request.POST)

        #----------------------------------------------------------------------
        # If the event name as delivered by the request is 'No Event defined'
        # then just return
        #----------------------------------------------------------------------
        if fault_form['fault_name'].value() == 'No Events defined':
           return HttpResponseRedirect('../faults/')

        if fault_form.is_valid():
            #------------------------------------------------------------------
            # The form is valid, so process the data in form.cleaned_data
            # to extract the event and send to the backend.
            #------------------------------------------------------------------
            events_to_send = fault_form.cleaned_data['fault_count']
            event_rate = fault_form.cleaned_data['fault_rate']
            name = fault_form.cleaned_data['fault_name']
            fault = Fault.objects.get(fault_name=name)
            additional_info = fault.faultadditionalinfo_set.all()
            command = {'action': 'raise_fault',
                       'fault': {
                             'alarm_condition': fault.alarm_condition,
                             'event_type': fault.event_type,
                             'severity': fault.severity,
                             'specific_problem': fault.specific_problem,
                             'alarm_a_interface': fault.alarm_a_interface,
                             'additional_info': [(info.name, info.value)
                                                   for info in additional_info]
                                 },
                       'vnf_overrides': {
                             'function_role': fault.override_function_role,
                             'reporting_entity_id':
                                        fault.override_reporting_entity_id,
                             'reporting_entity_name':
                                        fault.override_reporting_entity_name,
                             'source_id': fault.override_source_id,
                             'source_name': fault.override_source_name
                             },
                       'fault_count': events_to_send,
                       'fault_rate': event_rate,
                    }

            request.session['fault_count'] = events_to_send
            request.session['fault_rate'] = event_rate
            request.session['fault_name'] = name

            #------------------------------------------------------------------
            # Establish a connection to our backend.  In general, this should
            # always succeed because the backend is colocated, but mis-config
            # or failure of the backend can still occur.
            #------------------------------------------------------------------
            posted_ok = True
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                try:
                    s.connect(('127.0.0.1', 27113))
                    s.sendall(json.dumps(command))
                    increment_total_events(events_to_send)

                except socket.error as e:
                    logger.error('Unexpected error: {}'.format(
                                                           sys.exc_info()[0]))
                    posted_ok = False

                s.close()

            except socket.error as e:
                logger.error('Unexpected error: {}'.format(sys.exc_info()[0]))
                posted_ok = False

            #------------------------------------------------------------------
            # Redirect to a new URL depending whether we successfully delivered
            # the event.
            #------------------------------------------------------------------
            return HttpResponseRedirect('./thanks/') if posted_ok \
              else HttpResponseRedirect('./failed/')
        else:
            #------------------------------------------------------------------
            # Bad data in the form
            #------------------------------------------------------------------
            logger.warning('Data in the form failed to validate')
            raise RuntimeError('Failed to validate data')
            return HttpResponseRedirect('./failed/')

    #--------------------------------------------------------------------------
    # If a GET (or any other method) we'll create a blank form
    #--------------------------------------------------------------------------
    else:
        count = request.session.get('fault_count', 1)
        rate = request.session.get('fault_rate', 0.1)
        name = request.session.get('fault_name', None)

        #----------------------------------------------------------------------
        # If there are no events defined, set the stored event name to be None.
        # If the stored event name doesn't exist in the set, go for the first
        # event
        # If there is no stored name, set the selection to be the first event
        # in the list
        #----------------------------------------------------------------------
        if len(Fault.objects.all()) < 1:
            name = None
            request.session['fault_name'] = name
        elif (len(Fault.objects.filter(fault_name=name)) == 0):
             name = Fault.objects.all()[0]
        elif name is None:
            name = Fault.objects.all()[0]

        initial_values = {'fault_name': name,
                          'fault_count': count,
                          'fault_rate': rate}
        fault_form = FaultForm(initial_values)

    context = {'title': banner,
               'fault_form': fault_form,
               'total_events': get_total_events()}

    return render(request, 'reporting_app/fault.html', context)

def raise_measurement(request):
    if request.method == 'POST':
        #----------------------------------------------------------------------
        # If this is a POST request we need to process the form data
        # create a form instance and populate it with data from the request,
        # checking whether it's valid.
        #----------------------------------------------------------------------
        measurement_form = MeasurementForm(request.POST)

        #----------------------------------------------------------------------
        # If the event name as delivered by the request is 'No Events defined'
        # then just return
        #----------------------------------------------------------------------
        if measurement_form['measurement'].value() == 'No Events defined':
           return HttpResponseRedirect('../measurements/')

        if measurement_form.is_valid():
            #------------------------------------------------------------------
            # The form is valid, so process the data in form.cleaned_data
            # to extract the details of the meas event. Note that this
            # includes walking the relationships to all of the linked models.
            #------------------------------------------------------------------
            events_to_send = measurement_form.cleaned_data['measurement_count']
            event_rate = measurement_form.cleaned_data['measurement_rate']
            name = measurement_form.cleaned_data['measurement']
            meas = Measurement.objects.get(measurement_name=name)
            addl_meas_grps = []
            for grp in meas.measurementadditionalmeasurementgroup_set.all():
                meas_grp = {'name': grp.name}
                meas_grp['fields'] = [{'name': grp.name_1,
                                       'value': grp.value_1},
                                      {'name': grp.name_2,
                                       'value': grp.value_2},
                                      {'name': grp.name_3,
                                       'value': grp.value_3},
                                      {'name': grp.name_4,
                                       'value': grp.value_4}
                                      ]
                addl_meas_grps.append(meas_grp)

            codecs_in_use = [(o.identifier, o.utilization) for o in
                                       meas.measurementcodecinuse_set.all()]
            features_in_use = [(o.identifier, o.utilization) for o in
                                       meas.measurementfeatureinuse_set.all()]
            file_system_use = []
            for fs in meas.measurementfilesystemuse_set.all():
                fsu = {}
                fsu['identifier'] = unicode(fs.identifier)
                fsu['block_configured'] = fs.block_configured
                fsu['block_iops'] = fs.block_iops
                fsu['block_used'] = fs.block_used
                fsu['ephemeral_configured'] = fs.ephemeral_configured
                fsu['ephemeral_iops'] = fs.ephemeral_iops
                fsu['ephemeral_used'] = fs.ephemeral_used
                file_system_use.append(fsu)

            latency_distribution = []
            for latency in meas.measurementlatencydistribution_set.all():
                ld = {}
                ld['low_end'] = latency.low_end
                ld['high_end'] = latency.high_end
                ld['count'] = latency.count
                latency_distribution.append(ld)

            vnic_use = []
            for vnic in meas.measurementvnicuse_set.all():
                vu = {}
                vu['identifier'] = vnic.identifier
                vu['broadcast_packets_in'] = vnic.broadcast_packets_in
                vu['broadcast_packets_out'] = vnic.broadcast_packets_out
                vu['bytes_in'] = vnic.bytes_in
                vu['bytes_out'] = vnic.bytes_out
                vu['multicast_packets_in'] = vnic.multicast_packets_in
                vu['multicast_packets_out'] = vnic.multicast_packets_out
                vu['unicast_packets_in'] = vnic.unicast_packets_in
                vu['unicast_packets_out'] = vnic.unicast_packets_out
                vnic_use.append(vu)

            cpu_use = [(o.identifier, o.utilization) for o in
                                       meas.measurementcpuuse_set.all()]

            #------------------------------------------------------------------
            # Build up the message itself.
            #------------------------------------------------------------------
            command = {'action': 'raise_measurement',
                       'measurement': {
                             'aggregate_cpu_usage': meas.aggregate_cpu_usage,
                             'concurrent_sessions': meas.concurrent_sessions,
                             'configured_entities': meas.configured_entities,
                             'mean_request_latency': meas.mean_request_latency,
                             'measurement_interval': meas.measurement_interval,
                             'memory_configured': meas.memory_configured,
                             'memory_used': meas.memory_used,
                             'media_ports_in_use': meas.media_ports_in_use,
                             'request_rate': meas.request_rate,
                             'scaling_metric': meas.scaling_metric,
                             'additional_measurement_groups': addl_meas_grps,
                             'codecs_in_use': codecs_in_use,
                             'features_in_use': features_in_use,
                             'file_system_use': file_system_use,
                             'latency_distribution': latency_distribution,
                             'vnic_use': vnic_use,
                             'cpu_use': cpu_use,
                             },
                       'vnf_overrides': {
                             'function_role': meas.override_function_role,
                             'reporting_entity_id':
                                        meas.override_reporting_entity_id,
                             'reporting_entity_name':
                                        meas.override_reporting_entity_name,
                             'source_id': meas.override_source_id,
                             'source_name': meas.override_source_name
                             },
                       'measurement_count': events_to_send,
                       'measurement_rate': event_rate,
                    }

            request.session['measurement_count'] = events_to_send
            request.session['measurement_rate'] = event_rate
            request.session['measurement_name'] = name

            #------------------------------------------------------------------
            # Establish a connection to our backend.  In general, this should
            # always succeed because the backend is colocated, but mis-config
            # or failure of the backend can still occur.
            #------------------------------------------------------------------
            posted_ok = True
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                try:
                    s.connect(('127.0.0.1', 27113))
                    s.sendall(json.dumps(command))
                    increment_total_events(events_to_send)

                except socket.error as e:
                    logger.error('Unexpected error: {}'.format(
                                                           sys.exc_info()[0]))
                    posted_ok = False

                s.close()

            except socket.error as e:
                logger.error('Unexpected error: {}'.format(sys.exc_info()[0]))
                posted_ok = False

            #------------------------------------------------------------------
            # Redirect to a new URL depending whether we successfully delivered
            # the event.
            #------------------------------------------------------------------
            return HttpResponseRedirect('./thanks/') if posted_ok \
              else HttpResponseRedirect('./failed/')
        else:
            #------------------------------------------------------------------
            # Bad data in the form
            #------------------------------------------------------------------
            logger.warning('Data in the form failed to validate')
            return HttpResponseRedirect('./failed/')

    #--------------------------------------------------------------------------
    # If a GET (or any other method) we'll create a blank form
    #--------------------------------------------------------------------------
    else:
        count = request.session.get('measurement_count', 1)
        rate = request.session.get('measurement_rate', 0.1)
        name = request.session.get('measurement_name', None)

        #----------------------------------------------------------------------
        # If there are no events defined, set the stored event name to be None.
        # If the stored event name doesn't exist in the set, go for the first
        # event
        # If there is no stored name, set the selection to be the first event
        # in the list
        #----------------------------------------------------------------------
        if len(Measurement.objects.all()) < 1:
            name = None
            request.session['measurement_name'] = name
        elif (len(Measurement.objects.filter(measurement_name=name)) == 0):
             name = Measurement.objects.all()[0]
        elif name is None:
            name = Measurement.objects.all()[0]

        initial_values = {'measurement': name,
                          'measurement_count': count,
                          'measurement_rate': rate}
        measurement_form = MeasurementForm(initial_values)

    context = {'title': banner,
               'measurement_form': measurement_form,
               'total_events': get_total_events()}

    return render(request, 'reporting_app/measurement.html', context)

def index(request):
    return render(request, 'reporting_app/index.html', {'title': banner})

def posted(request):
    return render(request, 'reporting_app/posted.html', {'title': banner})

def failed(request):
    return render(request, 'reporting_app/failed.html', {'title': banner})

def lifecycle(request):
    if (request.method == 'POST'):
        #----------------------------------------------------------------------
        # If this is a POST request we need to process the form data
        # create a form instance and populate it with data from the request,
        # checking whether it's valid.
        #----------------------------------------------------------------------
        lifecycle_form = LifecycleForm(request.POST)
        if lifecycle_form.is_valid():
            #------------------------------------------------------------------
            # The form is valid, so process the data in form.cleaned_data
            # to extract the event and send to the backend. We need to
            # determine which button was pressed.
            #------------------------------------------------------------------
            if ('terminate' in request.POST):
                logger.info('Terminate request received')
                dwell_time = lifecycle_form.cleaned_data['dwell_time']
                command = {'action': 'prepare_terminate',
                           'dwell_time':
                                     lifecycle_form.cleaned_data['dwell_time'],
                        }
            elif ('activate' in request.POST):
                logger.info('Activate request received')
                command = {'action': 'activate'}
            else:
                raise RuntimeError('Unexpected POST received!')

            #------------------------------------------------------------------
            # Establish a connection to our backend.  In general, this should
            # always succeed because the backend is colocated, but mis-config
            # or failure of the backend can still occur.
            #------------------------------------------------------------------
            posted_ok = True
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                try:
                    s.connect(('127.0.0.1', 27113))
                    s.sendall(json.dumps(command))

                except socket.error as e:
                    logger.error('Unexpected error: {}'.format(
                                                           sys.exc_info()[0]))
                    posted_ok = False

                s.close()

            except socket.error as e:
                logger.error('Unexpected error: {}'.format(sys.exc_info()[0]))
                posted_ok = False

            #------------------------------------------------------------------
            # Redirect to a new URL depending whether we successfully delivered
            # the event.
            #------------------------------------------------------------------
            return HttpResponseRedirect('./thanks/') if posted_ok \
              else HttpResponseRedirect('./failed/')
        else:
            #------------------------------------------------------------------
            # Bad data in the form
            #------------------------------------------------------------------
            logger.warning('Data in the form failed to validate')
            return HttpResponseRedirect('./failed/')

    #--------------------------------------------------------------------------
    # If a GET (or any other method) we'll create a blank form
    #--------------------------------------------------------------------------
    else:
        initial_values = {'dwell_time': 10}
        lifecycle_form = LifecycleForm(initial_values)

    context = {'title': banner,
               'lifecycle_form': lifecycle_form,
               'total_events': get_total_events()}

    return render(request, 'reporting_app/lifecycle.html', context)

def raise_mobile_flow(request):
    if request.method == 'POST':
        #----------------------------------------------------------------------
        # If this is a POST request we need to process the form data
        # create a form instance and populate it with data from the request,
        # checking whether it's valid.
        #----------------------------------------------------------------------
        mobile_flow_form = MobileFlowForm(request.POST)

        #----------------------------------------------------------------------
        # If the event name as delivered by the request is 'No Events defined'
        # then just return
        #----------------------------------------------------------------------
        if mobile_flow_form['mobile_flow'].value() == 'No Events defined':
           return HttpResponseRedirect('../mobile_flow/')

        if mobile_flow_form.is_valid():
            #------------------------------------------------------------------
            # The form is valid, so process the data in form.cleaned_data
            # to extract the event and send to the backend.
            #------------------------------------------------------------------
            events_to_send = mobile_flow_form.cleaned_data['mobile_flow_count']
            event_rate = mobile_flow_form.cleaned_data['mobile_flow_rate']
            friendly_name = mobile_flow_form.cleaned_data['mobile_flow']
            mobile_flow = MobileFlow.objects.get(friendly_name=friendly_name)

            ip_tos_count = mobile_flow.gtpmetriciptoscount_set.all()
            gtp_tcp_flag_count = mobile_flow.gtpmetrictcpflagcount_set.all()
            gtp_mobile_qci_cos_count = \
                               mobile_flow.gtpmetricmobileqcicoscount_set.all()

            gtp_metric_ip_tos = mobile_flow.gtpmetriciptos_set.all()
            gtp_metric_mobile_qci_cos = \
                                    mobile_flow.gtpmetricmobileqcicos_set.all()
            gtp_metric_tcp_flag = mobile_flow.gtpmetrictcpflag_set.all()

            command = {'action': 'raise_mobile_flow',
                       'mobile_flow' :
                       {
                        'flow_direction': mobile_flow.flow_direction,
                        'ip_protocol_type': mobile_flow.ip_protocol_type,
                        'ip_version': mobile_flow.ip_version,
                        'other_endpoint_ip_address':
                                         mobile_flow.other_endpoint_ip_address,
                        'other_endpoint_port':
                                               mobile_flow.other_endpoint_port,
                        'reporting_endpoint_ip_addr':
                                        mobile_flow.reporting_endpoint_ip_addr,
                        'reporting_endpoint_port':
                                           mobile_flow.reporting_endpoint_port,
                        'application_type': mobile_flow.application_type,
                        'app_protocol_type': mobile_flow.app_protocol_type,
                        'app_protocol_version':
                                              mobile_flow.app_protocol_version,
                        'cid': mobile_flow.cid,
                        'connection_type': mobile_flow.connection_type,
                        'ecgi': mobile_flow.ecgi,
                        'gtp_protocol_type': mobile_flow.gtp_protocol_type,
                        'gtp_version': mobile_flow.gtp_version,
                        'http_header': mobile_flow.http_header,
                        'imei': mobile_flow.imei,
                        'imsi': mobile_flow.imsi,
                        'lac': mobile_flow.lac,
                        'mcc': mobile_flow.mcc,
                        'mnc': mobile_flow.mnc,
                        'msisdn': mobile_flow.msisdn,
                        'other_functional_role':
                                             mobile_flow.other_functional_role,
                        'rac': mobile_flow.rac,
                        'radio_access_technology':
                                           mobile_flow.radio_access_technology,
                        'sac': mobile_flow.sac,
                        'sampling_algorithm': mobile_flow.sampling_algorithm,
                        'tac': mobile_flow.tac,
                        'tunnel_id': mobile_flow.tunnel_id,
                        'vlan_id': mobile_flow.vlan_id,
                        # GTP Per Flow Metrics fields
                        'avg_bit_error_rate': mobile_flow.avg_bit_error_rate,
                        'avg_packet_delay_variation':
                                        mobile_flow.avg_packet_delay_variation,
                        'avg_packet_latency': mobile_flow.avg_packet_latency,
                        'avg_receive_throughput':
                                            mobile_flow.avg_receive_throughput,
                        'avg_transmit_throughput':
                                           mobile_flow.avg_transmit_throughput,
                        'flow_activation_epoch':
                                             mobile_flow.flow_activation_epoch,
                        'flow_activation_microsec':
                                          mobile_flow.flow_activation_microsec,
                        'flow_deactivation_epoch':
                                           mobile_flow.flow_deactivation_epoch,
                        'flow_deactivation_microsec':
                                        mobile_flow.flow_deactivation_microsec,
                        'flow_deactivation_time':
                                            mobile_flow.flow_deactivation_time,
                        'flow_status': mobile_flow.flow_status,
                        'max_packet_delay_variation':
                                        mobile_flow.max_packet_delay_variation,
                        'num_activation_failures':
                                           mobile_flow.num_activation_failures,
                        'num_bit_errors': mobile_flow.num_bit_errors,
                        'num_bytes_received': mobile_flow.num_bytes_received,
                        'num_bytes_transmitted':
                                             mobile_flow.num_bytes_transmitted,
                        'num_dropped_packets': mobile_flow.num_dropped_packets,
                        'num_L7_bytes_received':
                                             mobile_flow.num_L7_bytes_received,
                        'num_L7_bytes_transmitted':
                                          mobile_flow.num_L7_bytes_transmitted,
                        'num_lost_packets': mobile_flow.num_lost_packets,
                        'num_out_of_order_packets':
                                          mobile_flow.num_out_of_order_packets,
                        'num_packet_errors': mobile_flow.num_packet_errors,
                        'num_packets_received_excl_retrans':
                                 mobile_flow.num_packets_received_excl_retrans,
                        'num_packets_received_incl_retrans':
                                mobile_flow.num_packets_received_incl_retrans,
                        'num_packets_transmitted_incl_retrans':
                              mobile_flow.num_packets_transmitted_incl_retrans,
                        'num_retries': mobile_flow.num_retries,
                        'num_timeouts': mobile_flow.num_timeouts,
                        'num_tunneled_L7_bytes_received':
                                    mobile_flow.num_tunneled_L7_bytes_received,
                        'round_trip_time': mobile_flow.round_trip_time,
                        'time_to_first_byte': mobile_flow.time_to_first_byte,
                        'dur_connection_failed_status':
                                      mobile_flow.dur_connection_failed_status,
                        'dur_tunnel_failed_status':
                                          mobile_flow.dur_tunnel_failed_status,
                        'flow_activated_by': mobile_flow.flow_activated_by,
                        'flow_activation_time':
                                              mobile_flow.flow_activation_time,
                        'flow_deactivated_by': mobile_flow.flow_deactivated_by,
                        'gtp_connection_status':
                                             mobile_flow.gtp_connection_status,
                        'gtp_tunnel_status': mobile_flow.gtp_tunnel_status,
                        'large_packet_rtt': mobile_flow.large_packet_rtt,
                        'large_packet_threshold':
                                            mobile_flow.large_packet_threshold,
                        'max_receive_bit_rate':
                                              mobile_flow.max_receive_bit_rate,
                        'max_transmit_bit_rate':
                                             mobile_flow.max_transmit_bit_rate,
                        'num_gtp_echo_failures':
                                             mobile_flow.num_gtp_echo_failures,
                        'num_gtp_tunnel_errors':
                                             mobile_flow.num_gtp_tunnel_errors,
                        'num_http_errors': mobile_flow.num_gtp_tunnel_errors,

                        'ip_tos_count_list': [(tos_count.key,
                                               tos_count.value)
                                                for tos_count in ip_tos_count],

                        'tcp_flag_count_list': [(flag_count.key,
                                                 flag_count.value)
                                         for flag_count in gtp_tcp_flag_count],

                        'mobile_qci_cos_count_list': [(qci_cos_count.key,
                                                       qci_cos_count.value)
                                for qci_cos_count in gtp_mobile_qci_cos_count],

                        'tcp_flag_list': [flag.value
                                              for flag in gtp_metric_tcp_flag],

                        'ip_tos_list': [tos.value
                                                 for tos in gtp_metric_ip_tos],

                        'mobile_qci_cos_list': [qci_cos.value
                                     for qci_cos in gtp_metric_mobile_qci_cos],
                        },
                       'vnf_overrides': {
                             'function_role':
                                    mobile_flow.override_function_role,
                             'reporting_entity_id':
                                    mobile_flow.override_reporting_entity_id,
                             'reporting_entity_name':
                                    mobile_flow.override_reporting_entity_name,
                             'source_id': mobile_flow.override_source_id,
                             'source_name': mobile_flow.override_source_name
                             },
                       'mobile_flow_count': events_to_send,
                       'mobile_flow_rate': event_rate,
                    }

            request.session['mobile_flow_count'] = events_to_send
            request.session['mobile_flow_rate'] = event_rate
            request.session['mobile_flow_name'] = friendly_name

            #------------------------------------------------------------------
            # Establish a connection to our backend.  In general, this should
            # always succeed because the backend is colocated, but mis-config
            # or failure of the backend can still occur.
            #------------------------------------------------------------------
            posted_ok = True
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                try:
                    s.connect(('127.0.0.1', 27113))
                    s.sendall(json.dumps(command))
                    increment_total_events(events_to_send)

                except socket.error as e:
                    logger.error('Unexpected error: {}'.format(
                                                           sys.exc_info()[0]))
                    posted_ok = False

                s.close()

            except socket.error as e:
                logger.error('Unexpected error: {}'.format(sys.exc_info()[0]))
                posted_ok = False

            #------------------------------------------------------------------
            # Redirect to a new URL depending whether we successfully delivered
            # the event.
            #------------------------------------------------------------------
            return HttpResponseRedirect('./thanks/') if posted_ok \
              else HttpResponseRedirect('./failed/')
        else:
            #------------------------------------------------------------------
            # Bad data in the form
            #------------------------------------------------------------------
            logger.warning('Data in the form failed to validate')
            raise RuntimeError('Failed to validate data')
            return HttpResponseRedirect('./failed/')

    #--------------------------------------------------------------------------
    # If a GET (or any other method) we'll create a blank form
    #--------------------------------------------------------------------------
    else:
        count = request.session.get('mobile_flow_count', 1)
        rate = request.session.get('mobile_flow_rate', 0.1)
        name = request.session.get('mobile_flow_name', None)

        #----------------------------------------------------------------------
        # If there are no events defined, set the stored event name to be None.
        # If the stored event name doesn't exist in the set, go for the first
        # event
        # If there is no stored name, set the selection to be the first event
        # in the list
        #----------------------------------------------------------------------
        if len(MobileFlow.objects.all()) < 1:
            name = None
            request.session['mobile_flow_name'] = name
        elif (len(MobileFlow.objects.filter(friendly_name=name)) == 0):
             name = MobileFlow.objects.all()[0]
        elif name is None:
            name = MobileFlow.objects.all()[0]

        initial_values = {'mobile_flow': name,
                          'mobile_flow_count': count,
                          'mobile_flow_rate': rate}
        mobile_flow_form = MobileFlowForm(initial_values)

    context = {'title': banner,
               'mobile_flow_form': mobile_flow_form,
               'total_events': get_total_events()}

    return render(request, 'reporting_app/mobile_flow.html', context)

def raise_syslog(request):
    if request.method == 'POST':
        #----------------------------------------------------------------------
        # If this is a POST request we need to process the form data
        # create a form instance and populate it with data from the request,
        # checking whether it's valid.
        #----------------------------------------------------------------------
        syslog_form = SyslogForm(request.POST)

        #----------------------------------------------------------------------
        # If the event name as delivered by the request is 'No Events defined'
        # then just return
        #----------------------------------------------------------------------
        if syslog_form['syslog'].value() == 'No Events defined':
           return HttpResponseRedirect('../syslog/')

        if syslog_form.is_valid():
            #------------------------------------------------------------------
            # The form is valid, so process the data in form.cleaned_data
            # to extract the event and send to the backend.
            #------------------------------------------------------------------
            events_to_send = syslog_form.cleaned_data['syslog_count']
            event_rate = syslog_form.cleaned_data['syslog_rate']
            friendly_name = syslog_form.cleaned_data['syslog']
            syslog = Syslog.objects.get(friendly_name=friendly_name)

            command = {'action': 'raise_syslog',
                       'syslog' :
                       {
                         'syslog_tag': syslog.syslog_tag,
                         'syslog_msg': syslog.syslog_msg,
                         'event_source_host': syslog.event_source_host,
                         'syslog_facility': syslog.syslog_facility,
                         'syslog_proc': syslog.syslog_proc,
                         'syslog_proc_id': syslog.syslog_proc_id,
                         'syslog_ver': syslog.syslog_ver,
                         'syslog_sdata': syslog.syslog_sdata,
                        },
                       'vnf_overrides': {
                             'function_role': syslog.override_function_role,
                             'reporting_entity_id':
                                        syslog.override_reporting_entity_id,
                             'reporting_entity_name':
                                        syslog.override_reporting_entity_name,
                             'source_id': syslog.override_source_id,
                             'source_name': syslog.override_source_name
                             },
                       'syslog_count': events_to_send,
                       'syslog_rate': event_rate,
                    }

            request.session['syslog_count'] = events_to_send
            request.session['syslog_rate'] = event_rate
            request.session['syslog_name'] = friendly_name
            #------------------------------------------------------------------
            # Establish a connection to our backend.  In general, this should
            # always succeed because the backend is colocated, but mis-config
            # or failure of the backend can still occur.
            #------------------------------------------------------------------
            posted_ok = True
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                try:
                    s.connect(('127.0.0.1', 27113))
                    s.sendall(json.dumps(command))
                    increment_total_events(events_to_send)

                except socket.error as e:
                    logger.error('Unexpected error: {}'.format(
                                                           sys.exc_info()[0]))
                    posted_ok = False


                s.close()

            except socket.error as e:
                logger.error('Unexpected error: {}'.format(sys.exc_info()[0]))
                posted_ok = False

            #------------------------------------------------------------------
            # Redirect to a new URL depending whether we successfully delivered
            # the event.
            #------------------------------------------------------------------
            return HttpResponseRedirect('./thanks/') if posted_ok \
              else HttpResponseRedirect('./failed/')
        else:
            #------------------------------------------------------------------
            # Bad data in the form
            #------------------------------------------------------------------
            logger.warning('Data in the form failed to validate')
            raise RuntimeError('Failed to validate data')
            return HttpResponseRedirect('./failed/')

    #--------------------------------------------------------------------------
    # If a GET (or any other method) we'll create a blank form
    #--------------------------------------------------------------------------
    else:
        count = request.session.get('syslog_count', 1)
        rate = request.session.get('syslog_rate', 0.1)
        name = request.session.get('syslog_name', None)

        #----------------------------------------------------------------------
        # If there are no events defined, set the stored event name to be None.
        # If the stored event name doesn't exist in the set, go for the first
        # event
        # If there is no stored name, set the selection to be the first event
        # in the list
        #----------------------------------------------------------------------
        if len(Syslog.objects.all()) < 1:
            name = None
            request.session['syslog_name'] = name
        elif (len(Syslog.objects.filter(friendly_name=name)) == 0):
            name = Syslog.objects.all()[0]
        elif name is None:
            name = Syslog.objects.all()[0]

        initial_values = {'syslog': name,
                          'syslog_count': count,
                          'syslog_rate': rate}
        syslog_form = SyslogForm(initial_values)

    context = {'title': banner,
               'syslog_form': syslog_form,
               'total_events': get_total_events()}

    return render(request, 'reporting_app/syslog.html', context)

def increment_total_events(events_sent):
    '''increment the total_events count by the number of events sent
    '''
    event_counter = EventCounter.objects.get_or_create(
                                                  event_type='total_events')[0]
    event_counter.count = F('count') + events_sent
    event_counter.save()
    return

def get_total_events():
    '''get the current value of 'total_events' sent
    '''
    event_counter = \
               EventCounter.objects.get_or_create(event_type='total_events')[0]
    return event_counter.count

def clear_events():
    '''set the current value of 'total_events' sent to be 0
    '''
    event_counter = EventCounter.objects.get_or_create(
                                                  event_type='total_events')[0]
    event_counter.count = 0
    event_counter.save()
    return
