#!/usr/bin/env python
'''
Define the data model for Django.
'''

from django.db import models
from .singleton_model import SingletonModel

#------------------------------------------------------------------------------
# Create your models here.
#------------------------------------------------------------------------------
class ReportingAppConfig(SingletonModel):
    ''' The application configuration table.
    '''
    class Meta:
        verbose_name = 'event reporting application configuration'
        verbose_name_plural = verbose_name

    collector_url = models.URLField(max_length=200)
    topology = models.CharField(max_length=20,
                                choices=[('SINGLETON', 'Singleton'),
                                         ('HA-PAIR', 'HA Pair'),
                                         ('CLUSTER', 'Cluster')])

class EventCounter(models.Model):
    ''' Counts of events
    Initially only the total events sent are recorded.
    '''
    class Meta:
        verbose_name = 'event counts'
        verbose_name_plural = verbose_name

    event_type = models.CharField(max_length=64, default=None)
    count = models.IntegerField(default=0)

class Fault(models.Model):
    ''' The Fault type of event.

    The Alarm Condition is used as the unique ID for the Fault and is
    therefore its primary key.  Note that it is not obvious from the AT&T
    documentation that this is necessarily correct.

    Note that the Event Header is not modelled separately but is included
    in the objects.
    '''
    class Meta:
        ordering = ['fault_name']

    fault_name = models.CharField(max_length=64, primary_key=True)

    event_type = models.CharField(max_length=64,
                                  blank=True,
                                  default=u'unknown')
    severity = models.CharField(max_length=16,
                                choices=[('CRITICAL', 'Critical'),
                                           ('MAJOR', 'Major'),
                                           ('MINOR', 'Minor'),
                                           ('WARNING', 'Warning'),
                                           ('NORMAL', 'Normal')],
                                default='Normal')
    alarm_condition = models.CharField(max_length=256)
    specific_problem = models.CharField(max_length=256, default=u'unknown')
    alarm_a_interface = models.CharField(max_length=64, blank=True)

    #--------------------------------------------------------------------------
    # The following are normally derived from the VNF itself and are fixed for
    # all events, but we allow them to be overridden for use in test
    # environments.
    #--------------------------------------------------------------------------
    override_function_role = models.CharField(max_length=64, blank=True)
    override_reporting_entity_id = models.CharField(max_length=64, blank=True)
    override_reporting_entity_name = models.CharField(max_length=64,
                                                      blank=True)
    override_source_id = models.CharField(max_length=64, blank=True)
    override_source_name = models.CharField(max_length=64, blank=True)

    def __unicode__(self):
        return self.fault_name

class FaultAdditionalInfo(models.Model):
    ''' Additional, vendor-specific, fields that may be included in a Fault.

    Simply comprises an arbitrary number of Name-Value pairs.
    '''
    class Meta:
        ordering = ['name']

    fault = models.ForeignKey(Fault)
    name = models.CharField(max_length=64)
    value = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Measurement(models.Model):
    ''' The Measurement type of event.

    The data model doesn't have an obvious unique reference so we give the
    object a unique name that will be used as the primary key.

    Note that the Event Header is not modelled separately but is included
    in the objects.
    '''
    class Meta:
        ordering = ['measurement_name']

    measurement_name = models.CharField(max_length=64, primary_key=True)

    #--------------------------------------------------------------------------
    # Event Header fields
    #--------------------------------------------------------------------------
    event_type = models.CharField(max_length=64, blank=True)

    #--------------------------------------------------------------------------
    # Measurement fields
    #--------------------------------------------------------------------------
    aggregate_cpu_usage = models.FloatField(default=0)
    concurrent_sessions = models.IntegerField(default=0)
    configured_entities = models.IntegerField(default=0)
    mean_request_latency = models.FloatField(default=0)
    measurement_interval = models.FloatField(default=0)
    memory_configured = models.FloatField(default=0)
    memory_used = models.FloatField(default=0)
    media_ports_in_use = models.IntegerField(default=0)
    request_rate = models.IntegerField(default=0)
    scaling_metric = models.FloatField(default=0)

    #--------------------------------------------------------------------------
    # The following are normally derived from the VNF itself and are fixed for
    # all events, but we allow them to be overridden for use in test
    # environments.
    #--------------------------------------------------------------------------
    override_function_role = models.CharField(max_length=64, blank=True)
    override_reporting_entity_id = models.CharField(max_length=64, blank=True)
    override_reporting_entity_name = models.CharField(max_length=64,
                                                      blank=True)
    override_source_id = models.CharField(max_length=64, blank=True)
    override_source_name = models.CharField(max_length=64, blank=True)

    def __unicode__(self):
        return self.measurement_name


class MeasurementAdditionalMeasurementGroup(models.Model):
    ''' Additional, vendor-specific, fields that may be included in a
        Measurement.

        Because Django doesn't (comfortably) support nested inlines
        we denormalize the data and include a fixed number of measurements into
        the Measurement Group itself.
    '''
    class Meta:
        ordering = ['name']

    measurement = models.ForeignKey(Measurement)
    name = models.CharField(max_length=64)

    name_1 = models.CharField(max_length=64, blank=True)
    value_1 = models.CharField(max_length=64, blank=True)
    name_2 = models.CharField(max_length=64, blank=True)
    value_2 = models.CharField(max_length=64, blank=True)
    name_3 = models.CharField(max_length=64, blank=True)
    value_3 = models.CharField(max_length=64, blank=True)
    name_4 = models.CharField(max_length=64, blank=True)
    value_4 = models.CharField(max_length=64, blank=True)

    def __unicode__(self):
        return self.name

class MeasurementCodecInUse(models.Model):
    ''' Codec Utilisation.
     '''
    class Meta:
        ordering = ['identifier']

    measurement = models.ForeignKey(Measurement)
    identifier = models.CharField(max_length=64)
    utilization = models.IntegerField(default=0)

    def __unicode__(self):
        return self.identifier

class MeasurementFeatureInUse(models.Model):
    '''Feature Utilisation.
     '''
    class Meta:
        ordering = ['identifier']

    measurement = models.ForeignKey(Measurement)
    identifier = models.CharField(max_length=64)
    utilization = models.IntegerField(default=0)

    def __unicode__(self):
        return self.identifier

class MeasurementFileSystemUse(models.Model):
    '''File System Utilisation.
     '''
    class Meta:
        ordering = ['identifier']

    measurement = models.ForeignKey(Measurement)
    identifier = models.UUIDField()
    block_configured = models.IntegerField(default=0)
    block_iops = models.IntegerField(default=0)
    block_used = models.IntegerField(default=0)
    ephemeral_configured = models.IntegerField(default=0)
    ephemeral_iops = models.IntegerField(default=0)
    ephemeral_used = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.identifier)

class MeasurementLatencyDistribution(models.Model):
    '''Latency Bucket.
     '''
    class Meta:
        ordering = ['low_end']

    measurement = models.ForeignKey(Measurement)
    low_end = models.FloatField(default=0)
    high_end = models.FloatField(default=0)
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return u'{} - {}'.format(self.low_end, self.high_end)

class MeasurementVNICUse(models.Model):
    '''vNIC Utilisation.
     '''
    class Meta:
        ordering = ['identifier']

    measurement = models.ForeignKey(Measurement)
    identifier = models.CharField(max_length=64)
    broadcast_packets_in = models.IntegerField(default=0)
    broadcast_packets_out = models.IntegerField(default=0)
    bytes_in = models.IntegerField(default=0)
    bytes_out = models.IntegerField(default=0)
    multicast_packets_in = models.IntegerField(default=0)
    multicast_packets_out = models.IntegerField(default=0)
    unicast_packets_in = models.IntegerField(default=0)
    unicast_packets_out = models.IntegerField(default=0)

    def __unicode__(self):
        return self.identifier

class MeasurementCPUUse(models.Model):
    '''CPU Usage.
     '''
    class Meta:
        ordering = ['identifier']

    measurement = models.ForeignKey(Measurement)
    identifier = models.CharField(max_length=64)
    utilization = models.IntegerField(default=0)

    def __unicode__(self):
        return self.identifier

class MobileFlow(models.Model):
    '''The Mobile Flow type of event.

    Note that the Event Header is not modelled separately but is included
    in the objects.
    '''
    class Meta:
        ordering = ['friendly_name']

    friendly_name = models.CharField(max_length=64, primary_key=True)

    #--------------------------------------------------------------------------
    # ModelFlow required fields
    #--------------------------------------------------------------------------
    flow_direction = models.CharField(max_length=64,
                                      blank=True,
                                      default=u'unknown')
    ip_protocol_type = models.CharField(max_length=64,
                                        blank=True,
                                        default=u'unknown',
                                        verbose_name='IP protocol type')
    ip_version = models.CharField(max_length=64,
                                  blank=True,
                                  default=u'unknown',
                                        verbose_name='IP version')
    other_endpoint_ip_address = models.CharField(max_length=64,
                                                 blank=True,
                                                 default=u'unknown',
                                     verbose_name='Other endpoint IP address')
    other_endpoint_port = models.IntegerField(default=0)
    reporting_endpoint_ip_addr = models.CharField(max_length=64,
                                                  blank=True,
                                                  default=u'unknown')
    reporting_endpoint_port = models.IntegerField(default=0)

    #--------------------------------------------------------------------------
    # gtpPerFlowMetrics required fields
    #--------------------------------------------------------------------------
    avg_bit_error_rate = models.FloatField(default=0)
    avg_packet_delay_variation = models.IntegerField(default=0)
    avg_packet_latency = models.FloatField(default=0)
    avg_receive_throughput = models.FloatField(default=0)
    avg_transmit_throughput = models.FloatField(default=0)
    flow_activation_epoch = models.FloatField(default=0)
    flow_activation_microsec = models.IntegerField(default=0)
    flow_deactivation_epoch = models.FloatField(default=0)
    flow_deactivation_microsec = models.IntegerField(default=0)
    flow_deactivation_time = models.CharField(max_length=64,
                                              blank=True,
                                              default=u'unknown')
    flow_status = models.CharField(max_length=20,
                                   choices=[('WORKING', 'working'),
                                            ('INACTIVE', 'inactive'),
                                            ('FAILED', 'failed')])
    max_packet_delay_variation = models.IntegerField(default=0)
    num_activation_failures = models.IntegerField(default=0)
    num_bit_errors = models.IntegerField(default=0)
    num_bytes_received = models.IntegerField(default=0)
    num_bytes_transmitted = models.IntegerField(default=0)
    num_dropped_packets = models.IntegerField(default=0)
    num_L7_bytes_received = models.IntegerField(default=0,
                                          verbose_name='Num L7 bytes received')
    num_L7_bytes_transmitted = models.IntegerField(default=0,
                                    verbose_name='Num L7 bytes transmitted')
    num_lost_packets = models.IntegerField(default=0)
    num_out_of_order_packets = models.IntegerField(default=0)
    num_packet_errors = models.IntegerField(default=0)
    num_packets_received_excl_retrans = models.IntegerField(default=0)
    num_packets_received_incl_retrans = models.IntegerField(default=0)
    num_packets_transmitted_incl_retrans = models.IntegerField(default=0)
    num_retries = models.IntegerField(default=0)
    num_timeouts = models.IntegerField(default=0)
    num_tunneled_L7_bytes_received = models.IntegerField(default=0,
                                verbose_name='Num tunneled L7 bytes received')
    round_trip_time = models.FloatField(default=0)
    time_to_first_byte = models.FloatField(default=0)

    #--------------------------------------------------------------------------
    # gtpPerFlowMetrics optional fields
    #--------------------------------------------------------------------------
    dur_connection_failed_status = models.FloatField(blank=True, null=True)
    dur_tunnel_failed_status = models.FloatField(blank=True, null=True)
    flow_activated_by = models.CharField(max_length=64,
                                         blank=True,
                                         null=True)
    flow_activation_time = models.CharField(max_length=64,
                                            blank=True,
                                            null=True)
    flow_deactivated_by = models.CharField(max_length=64,
                                           blank=True,
                                           null=True)
    gtp_connection_status = models.CharField(max_length=64,
                                             blank=True,
                                             null=True,
                                          verbose_name='GTP connection status')
    gtp_tunnel_status = models.CharField(max_length=64,
                                         blank=True,
                                         null=True,
                                         verbose_name='GTP tunnel status')
    large_packet_rtt = models.FloatField(blank=True, null=True)
    large_packet_threshold = models.IntegerField(blank=True, null=True)
    max_receive_bit_rate = models.IntegerField(blank=True, null=True)
    max_transmit_bit_rate = models.IntegerField(blank=True, null=True)
    num_gtp_echo_failures = models.IntegerField(blank=True,
                                                null=True,
                                          verbose_name='Num GTP echo failures')
    num_gtp_tunnel_errors = models.IntegerField(blank=True, null=True)
    num_http_errors = models.IntegerField(blank=True,
                                          null=True,
                                          verbose_name='Num HTTP errors')

    #--------------------------------------------------------------------------
    # Mobile Flow optional fields
    #--------------------------------------------------------------------------
    application_type = models.CharField(max_length=64, blank=True, null=True)
    app_protocol_type = models.CharField(max_length=64, blank=True, null=True)
    app_protocol_version = models.CharField(max_length=64,
                                            blank=True,
                                            null=True)
    cid = models.CharField(max_length=64,
                           blank=True,
                           null=True,
                           verbose_name='CID')
    connection_type = models.CharField(max_length=64, blank=True, null=True)
    ecgi = models.CharField(max_length=64,
                            blank=True,
                            null=True,
                            verbose_name='ECGI')
    gtp_protocol_type = models.CharField(max_length=64,
                                         blank=True,
                                         null=True,
                                         verbose_name='GTP protocol type')
    gtp_version = models.CharField(max_length=64,
                                   blank=True,
                                   null=True,
                                   verbose_name='GTP version')
    http_header = models.CharField(max_length=64,
                                   blank=True,
                                   null=True,
                                   verbose_name='HTTP header')
    imei = models.CharField(max_length=64,
                            blank=True,
                            null=True,
                            verbose_name='IMEI')
    imsi = models.CharField(max_length=64,
                            blank=True,
                            null=True,
                            verbose_name='IMSI')
    lac = models.CharField(max_length=64,
                           blank=True,
                           null=True,
                           verbose_name='LAC')
    mcc = models.CharField(max_length=64,
                           blank=True,
                           null=True,
                           verbose_name='MCC')
    mnc = models.CharField(max_length=64,
                           blank=True,
                           null=True,
                           verbose_name='MNC')
    msisdn = models.CharField(max_length=64,
                              blank=True,
                              null=True,
                              verbose_name='MSISDN')
    other_functional_role = models.CharField(max_length=64,
                                             blank=True,
                                             null=True)
    rac = models.CharField(max_length=64,
                           blank=True,
                           null=True,
                           verbose_name='RAC')
    radio_access_technology = models.CharField(max_length=64,
                                               blank=True,
                                               null=True)
    sac = models.CharField(max_length=64,
                           blank=True,
                           null=True,
                           verbose_name='SAC')
    sampling_algorithm = models.IntegerField(blank=True, null=True)
    tac = models.CharField(max_length=64,
                           blank=True,
                           null=True,
                           verbose_name='TAC')
    tunnel_id = models.CharField(max_length=64,
                                 blank=True,
                                 null=True,
                                 verbose_name='Tunnel ID')
    vlan_id = models.CharField(max_length=64,
                               blank=True,
                               null=True,
                               verbose_name='VLAN ID')

    #--------------------------------------------------------------------------
    # The following are normally derived from the VNF itself and are fixed for
    # all events, but we allow them to be overridden for use in test
    # environments.
    #--------------------------------------------------------------------------
    override_function_role = models.CharField(max_length=64, blank=True)
    override_reporting_entity_id = models.CharField(max_length=64, blank=True)
    override_reporting_entity_name = models.CharField(max_length=64,
                                                      blank=True)
    override_source_id = models.CharField(max_length=64, blank=True)
    override_source_name = models.CharField(max_length=64, blank=True)

    def __unicode__(self):
        return self.friendly_name

class GtpMetricIpTosCount(models.Model):
    '''IP TOS Count.
     '''
    class Meta:
        ordering = ['key']

    gtp_per_flow_metrics = models.ForeignKey(MobileFlow)
    key = models.IntegerField(default=0)
    value = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.key)

class GtpMetricMobileQciCosCount(models.Model):
    '''QCI COS Count.
     '''
    class Meta:
        ordering = ['key']

    gtp_per_flow_metrics = models.ForeignKey(MobileFlow)
    key = models.CharField(max_length=64)
    value = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.key)

class GtpMetricTcpFlagCount(models.Model):
    '''TCP Flag Count.
     '''
    class Meta:
        ordering = ['key']

    gtp_per_flow_metrics = models.ForeignKey(MobileFlow)
    key = models.CharField(max_length=64)
    value = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.key)

class GtpMetricMobileQciCos(models.Model):
    '''QCI COS.
     '''
    class Meta:
        ordering = ['value']

    gtp_per_flow_metrics = models.ForeignKey(MobileFlow)
    value = models.CharField(max_length=64)

    def __unicode__(self):
        return unicode(self.value)

class GtpMetricTcpFlag(models.Model):
    '''TCP Flag.
     '''
    class Meta:
        ordering = ['value']

    gtp_per_flow_metrics = models.ForeignKey(MobileFlow)
    value = models.CharField(max_length=64)

    def __unicode__(self):
        return unicode(self.value)

class GtpMetricIpTos(models.Model):
    '''IP TOS.
     '''
    class Meta:
        ordering = ['value']

    gtp_per_flow_metrics = models.ForeignKey(MobileFlow)
    value = models.CharField(max_length=64)

    def __unicode__(self):
        return unicode(self.value)

class Syslog(models.Model):
    ''' The SysLog type of event.

    Note that the event Header is not modelled separately but is included
    in the objects.
    '''
    class Meta:
        ordering = ['friendly_name']

    friendly_name = models.CharField(max_length=64, primary_key=True)
    event_type = models.CharField(max_length=64, blank=True)

    #--------------------------------------------------------------------------
    # SysLog required fields
    #--------------------------------------------------------------------------
    syslog_tag = models.CharField(max_length=256,
                                  blank=True,
                                  default=u'unknown')
    syslog_msg = models.CharField(max_length=256,
                                  blank=True,
                                  default=u'unknown')
    #--------------------------------------------------------------------------
    # SysLog optional fields
    #--------------------------------------------------------------------------
    event_source_host = models.CharField(max_length=256,
                                         blank=True,
                                         null=True)
    syslog_facility = models.IntegerField(default=0)
    syslog_proc = models.CharField(max_length=256, blank=True, null=True)
    syslog_proc_id = models.IntegerField(default=0)
    syslog_ver = models.FloatField(default=0)
    syslog_sdata = models.CharField(max_length=256, blank=True, null=True)

    #--------------------------------------------------------------------------
    # The following are normally derived from the VNF itself and are fixed for
    # all events, but we allow them to be overridden for use in test
    # environments.
    #--------------------------------------------------------------------------
    override_function_role = models.CharField(max_length=64, blank=True)
    override_reporting_entity_id = models.CharField(max_length=64, blank=True)
    override_reporting_entity_name = models.CharField(max_length=64,
                                                      blank=True)
    override_source_id = models.CharField(max_length=64, blank=True)
    override_source_name = models.CharField(max_length=64, blank=True)

    def __unicode__(self):
        return self.friendly_name



