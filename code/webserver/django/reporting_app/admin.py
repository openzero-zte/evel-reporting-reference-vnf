#!/usr/bin/env python
'''
Define the administration interface to the data model for Django.
'''
from django.contrib import admin
import models

class FaultAdditionalInfoInline(admin.TabularInline):
    ''' Defines how we want to see Additional Info fields included
    in the Fault admin form.
    '''
    model = models.FaultAdditionalInfo
    verbose_name = 'Additional Information Field'
    verbose_name_plural = 'Additional Information Fields'
    extra = 1

class FaultAdmin(admin.ModelAdmin):
    '''Control how the admin of the Fault model is configured.
    '''

    #--------------------------------------------------------------------------
    # Layout of the admin page for an individual Fault.
    #--------------------------------------------------------------------------
    fieldsets = [
                    ('Header', {
                        'fields': ['fault_name',
                                   'event_type',
                                   'severity']}
                     ),
                 ('Fault Information', {
                        'fields': ['alarm_condition',
                                   'specific_problem',
                                   'alarm_a_interface'
                                   ]}),
                 ('VNF Environment Overrides', {
                        'fields': ['override_function_role',
                                   'override_reporting_entity_id',
                                   'override_reporting_entity_name',
                                   'override_source_id',
                                   'override_source_name'
                                    ]})
                 ]
    inlines = [FaultAdditionalInfoInline]

    #--------------------------------------------------------------------------
    # Which columns we want displayed in the "change" list display and how the
    # list may be filtered.
    #--------------------------------------------------------------------------
    list_display = ('fault_name',
                    'alarm_condition',
                    'specific_problem')
    list_filter = ['severity', 'event_type']

class MeasurementAdditionalMeasurementGroupInLine(admin.TabularInline):
    ''' Defines how we want to see Additional Measurement Group fields included
    in the Measurement admin form.
    '''
    model = models.MeasurementAdditionalMeasurementGroup
    verbose_name = 'Additional Measurement Group'
    verbose_name_plural = 'Additional Measurement Groups'
    extra = 1

class MeasurementCodecsInUseInLine(admin.TabularInline):
    ''' Defines how we want to see Codec Utilization fields included
    in the Measurement admin form.
    '''
    model = models.MeasurementCodecInUse
    verbose_name = 'Codec Utilization'
    verbose_name_plural = 'Codec Utilization'
    extra = 1

class MeasurementFeaturesInUseInLine(admin.TabularInline):
    ''' Defines how we want to see Codec Utilization fields included
    in the Measurement admin form.
    '''
    model = models.MeasurementFeatureInUse
    verbose_name = 'Feature Utilization'
    verbose_name_plural = 'Feature Utilization'
    extra = 1

class MeasurementFileSystemUseInLine(admin.TabularInline):
    ''' Defines how we want to see File System Utilization fields included
    in the Measurement admin form.
    '''
    model = models.MeasurementFileSystemUse
    verbose_name = 'File System Utilization'
    verbose_name_plural = 'File System Utilization'
    extra = 1

class MeasurementLatencyDistributionInLine(admin.TabularInline):
    ''' Defines how we want to see Latency Distribution fields included in the
    Measurement admin form.
    '''
    model = models.MeasurementLatencyDistribution
    verbose_name = 'Latency Distribution'
    verbose_name_plural = 'Latency Distribution'
    extra = 1

class MeasurementCPUUseInLine(admin.TabularInline):
    ''' Defines how we want to see CPU In Use fields included in the
    Measurement admin form.
    '''
    model = models.MeasurementCPUUse
    verbose_name = 'CPU Utilization'
    verbose_name_plural = 'CPU Utilization'
    extra = 1

class MeasurementVNICUseInLine(admin.TabularInline):
    ''' Defines how we want to see VNIC In Use fields included in the
    Measurement admin form.
    '''
    model = models.MeasurementVNICUse
    verbose_name = 'vNIC Utilization'
    verbose_name_plural = 'vNIC Utilization'
    extra = 1

class MeasurementAdmin(admin.ModelAdmin):
    '''Control how the admin of the Measurement model is configured.
    '''

    #--------------------------------------------------------------------------
    # Layout of the admin page for an individual Fault.
    #--------------------------------------------------------------------------
    fieldsets = [
                    ('Header', {
                        'fields': ['measurement_name',
                                   'event_type']}
                     ),
                     ('Measurement Information', {
                        'fields': ['aggregate_cpu_usage',
                           'concurrent_sessions',
                           'configured_entities',
                           'mean_request_latency',
                           'measurement_interval',
                           'memory_configured',
                           'memory_used',
                           'media_ports_in_use',
                           'request_rate',
                           'scaling_metric',
                           ]}),
                     ('VNF Environment Overrides', {
                        'fields': ['override_function_role',
                                   'override_reporting_entity_id',
                                   'override_reporting_entity_name',
                                   'override_source_id',
                                   'override_source_name'
                                    ]})
                 ]
    inlines = [MeasurementFeaturesInUseInLine,
               MeasurementCPUUseInLine,
               MeasurementFileSystemUseInLine,
               MeasurementVNICUseInLine,
               MeasurementCodecsInUseInLine,
               MeasurementLatencyDistributionInLine,
               MeasurementAdditionalMeasurementGroupInLine
               ]

    #--------------------------------------------------------------------------
    # Which columns we want displayed in the "change" list display and how the
    # list may be filtered.
    #--------------------------------------------------------------------------
    list_display = ('measurement_name',)

class GtpMetricIpTosCountInLine(admin.TabularInline):
    ''' Defines how we want to see IP TOS Count fields included in the
    Mobile Flow admin form.
    '''
    model = models.GtpMetricIpTosCount
    verbose_name = 'IP TOS count'
    verbose_name_plural = 'IP TOS counts'
    extra = 1

class GtpMetricIpTosInLine(admin.TabularInline):
    '''Defines how we want to see IP TOS fields included in the Mobile Flow
    admin form.
    '''
    model = models.GtpMetricIpTos
    verbose_name = 'IP TOS list'
    verbose_name_plural = 'IP TOS list'
    extra = 1

class GtpMetricMobileQciCosCountInLine(admin.TabularInline):
    '''Defines how we want to see Mobile QCI COS Count fields included in the
    Mobile Flow admin form.
    '''
    model = models.GtpMetricMobileQciCosCount
    verbose_name = 'Mobile QCI CoS count'
    verbose_name_plural = 'Mobile QCI CoS counts'
    extra = 1

class GtpMetricMobileQciCosInLine(admin.TabularInline):
    '''Defines how we want to see Mobile QCI COS fields included in the
    Mobile Flow admin form.
    '''
    model = models.GtpMetricMobileQciCos
    verbose_name = 'Mobile QCI CoS list'
    verbose_name_plural = 'Mobile QCI CoS lists'
    extra = 1

class GtpMetricTcpFlagCountInLine(admin.TabularInline):
    '''Defines how we want to see TCP Flag Count fields included in the
    Mobile Flow admin form.
    '''
    model = models.GtpMetricTcpFlagCount
    verbose_name = 'TCP flag count'
    verbose_name_plural = 'TCP flag counts'
    extra = 1

class GtpMetricTcpFlagInLine(admin.TabularInline):
    '''Defines how we want to see TCP Flag fields included in the Mobile Flow
    admin form.
    '''
    model = models.GtpMetricTcpFlag
    verbose_name = 'TCP flag list'
    verbose_name_plural = 'TCP flag lists'
    extra = 1

class MobileFlowAdmin(admin.ModelAdmin):
    '''Control how the admin of the Mobile Flow model is configured.
    '''

    #--------------------------------------------------------------------------
    # Layout of the admin page for a Mobile Flow.
    #--------------------------------------------------------------------------
    fieldsets = [
                    ('Header', {
                        'fields': ['friendly_name']}
                     ),
                     ('Flow details', {
                        'fields': [
                                    'flow_direction',
                                    'ip_protocol_type',
                                    'ip_version',
                                    'other_endpoint_ip_address',
                                    'other_endpoint_port',
                                    'reporting_endpoint_ip_addr',
                                    'reporting_endpoint_port',
                                    'application_type',
                                    'app_protocol_type',
                                    'app_protocol_version',
                                    'cid',
                                    'connection_type',
                                    'ecgi',
                                    'gtp_protocol_type',
                                    'gtp_version',
                                    'http_header',
                                    'imei',
                                    'imsi',
                                    'lac',
                                    'mcc',
                                    'mnc',
                                    'msisdn',
                                    'other_functional_role',
                                    'rac',
                                    'radio_access_technology',
                                    'sac',
                                    'sampling_algorithm',
                                    'tac',
                                    'tunnel_id',
                                    'vlan_id'
                                    ]}),

                     ('GTP per Flow Metrics', {
                        'fields': [
                                    'avg_packet_delay_variation',
                                    'avg_packet_latency',
                                    'avg_receive_throughput',
                                    'avg_transmit_throughput',
                                    'flow_activation_epoch',
                                    'flow_activation_microsec',
                                    'flow_deactivation_epoch',
                                    'flow_deactivation_microsec',
                                    'flow_deactivation_time',
                                    'flow_status',
                                    'max_packet_delay_variation',
                                    'num_activation_failures',
                                    'num_bit_errors',
                                    'num_bytes_received',
                                    'num_bytes_transmitted',
                                    'num_dropped_packets',
                                    'num_L7_bytes_received',
                                    'num_L7_bytes_transmitted',
                                    'num_lost_packets',
                                    'num_out_of_order_packets',
                                    'num_packet_errors',
                                    'num_packets_received_excl_retrans',
                                    'num_packets_received_incl_retrans',
                                    'num_packets_transmitted_incl_retrans',
                                    'num_retries',
                                    'num_timeouts',
                                    'num_tunneled_L7_bytes_received',
                                    'round_trip_time',
                                    'time_to_first_byte',
                                    'dur_connection_failed_status',
                                    'dur_tunnel_failed_status',
                                    'flow_activated_by',
                                    'flow_activation_time',
                                    'flow_deactivated_by',
                                    'gtp_connection_status',
                                    'gtp_tunnel_status',
                                    'large_packet_rtt',
                                    'large_packet_threshold',
                                    'max_receive_bit_rate',
                                    'max_transmit_bit_rate',
                                    'num_gtp_echo_failures',
                                    'num_gtp_tunnel_errors',
                                    'num_http_errors'
                                    ]}),
                     ('VNF Environment Overrides', {
                        'fields': ['override_function_role',
                                   'override_reporting_entity_id',
                                   'override_reporting_entity_name',
                                   'override_source_id',
                                   'override_source_name'
                                    ]})
                 ]
    inlines = [GtpMetricIpTosCountInLine,
               GtpMetricIpTosInLine,
               GtpMetricMobileQciCosCountInLine,
               GtpMetricMobileQciCosInLine,
               GtpMetricTcpFlagCountInLine,
               GtpMetricTcpFlagInLine,
            ]

    #--------------------------------------------------------------------------
    # Which columns we want displayed in the "change" list display and how the
    # list may be filtered.
    #--------------------------------------------------------------------------
    list_display = ('friendly_name',)

class SyslogAdmin(admin.ModelAdmin):
    '''Control how the admin of the Syslog model is configured.
    '''

    #--------------------------------------------------------------------------
    # Layout of the admin page for a Syslog
    #--------------------------------------------------------------------------
    fieldsets = [
                    ('Header', {
                        'fields': ['friendly_name']}
                     ),
                     ('Syslog details', {
                        'fields': [
                                    'syslog_tag',
                                    'syslog_msg',
                                    'event_source_host',
                                    'syslog_facility',
                                    'syslog_proc',
                                    'syslog_proc_id',
                                    'syslog_ver',
                                    'syslog_sdata',
                                    ]}),
                     ('VNF Environment Overrides', {
                        'fields': ['override_function_role',
                                   'override_reporting_entity_id',
                                   'override_reporting_entity_name',
                                   'override_source_id',
                                   'override_source_name'
                                    ]})
                 ]

    #--------------------------------------------------------------------------
    # Which columns we want displayed in the "change" list display and how the
    # list may be filtered.
    #--------------------------------------------------------------------------
    list_display = ('friendly_name',)
#------------------------------------------------------------------------------
# Register your models here.
#------------------------------------------------------------------------------
admin.site.site_header = 'AT&T Vendor Event Listener Service - ' \
                         'Reference VNF - Administration'
admin.site.register(models.ReportingAppConfig)
admin.site.register(models.Fault, FaultAdmin)
admin.site.register(models.Measurement, MeasurementAdmin)
admin.site.register(models.MobileFlow, MobileFlowAdmin)
admin.site.register(models.Syslog, SyslogAdmin)
