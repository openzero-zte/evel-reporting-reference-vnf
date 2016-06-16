#!/usr/bin/env python
'''
Forms defined for data entry in the Django framework.
'''
import logging
from django import forms
from models import Fault, Measurement, MobileFlow, Syslog

VNF_STATUSES = (
                ('I', 'Idle'),
                ('A', 'Active'),
                ('PTT', 'Preparing to Terminate'),
                ('RTT', 'Ready to Terminate'),
                ('RT', 'Requesting Termination')
               )

logger = logging.getLogger(__name__)

class FaultForm(forms.Form):
    ''' Fault Form

    Allows the user to choose a Fault and how many events to raise at a given
    rate.

    The constructor needs to initialize the Fault's fault_name choices so it
    reflects the state of the database at the point of use.
    '''

    def __init__(self, *args, **kwargs):
        '''Constructor to allocate dynamic choices.

        The constructor is needed to initialize the Alarm name choices so
        it reflects the state of the database at the point of use.
        '''
        super(FaultForm, self).__init__(*args, **kwargs)

        #----------------------------------------------------------------------
        # get the selected alarm_condition from the args. If there are no
        # faults defined in the database, the value will be None, so set the
        # text to read 'No Events defined'
        #----------------------------------------------------------------------
        fault_name = args[0]['fault_name']

        if fault_name is None:
            self.fields['fault_name'] = forms.CharField()
            self.fields['fault_name'].widget.attrs['readonly'] = True
            self.data['fault_name'] = 'No Events defined'
        else:
             self.fields['fault_name'] = forms.ChoiceField(choices=[
                     (o.fault_name, str(o)) for o in Fault.objects.all()])

        self.fields['fault_count'] = forms.IntegerField(
                                                    label='Faults to Raise',
                                                    min_value=1)
        self.fields['fault_rate'] = forms.FloatField(
                                                 label='Fault Rate (per sec)',
                                                 min_value=0.0,
                                                 max_value=10.0)

class MeasurementForm(forms.Form):
    ''' Measurement Form

    Allows the user to choose a Measurement and how many events to raise at a
    given rate.
    '''

    def __init__(self, *args, **kwargs):
        '''Constructor to allocate dynamic choices.

        The constructor is needed to initialize the Alarm Condition choices so
        it reflects the state of the database at the point of use.
        '''
        super(MeasurementForm, self).__init__(*args, **kwargs)

        #----------------------------------------------------------------------
        # get the selected event from the args. If there are no events defined
        # in the database, the value will be None, so set the text to read
        # 'No Events defined'
        #----------------------------------------------------------------------
        measurement_name = args[0]['measurement']

        if measurement_name is None:
            self.fields['measurement'] = forms.CharField()
            self.fields['measurement'].widget.attrs['readonly'] = True
            self.data['measurement'] = 'No Events defined'
        else:
             self.fields['measurement'] = forms.ChoiceField(choices=[
                     (o.measurement_name, str(o))
                        for o in Measurement.objects.all()])
        self.fields['measurement_count'] = forms.IntegerField(
                                              label='Measurements to Raise',
                                              min_value=1)
        self.fields['measurement_rate'] = forms.FloatField(
                                           label='Measurement Rate (per sec)',
                                           min_value=0.0,
                                           max_value=10.0)
        return

class LifecycleForm(forms.Form):
    '''Lifecycle Form

    Allows the user to manage the lifecycle of the VNF.
    '''

    dwell_time = forms.FloatField(label='Termination preparation time (secs)',
                                  min_value=0.0,
                                  max_value=3600.0)

class MobileFlowForm(forms.Form):
    ''' Mobile Flow  Form

    Allows the user to choose a Mobile Flow Object and how many events to raise
    at a given rate.
    '''

    def __init__(self, *args, **kwargs):
        '''Constructor to allocate dynamic choices.

        The constructor is needed to initialise the Metrics choices so
        it reflects the state of the database at the point of use.
        '''
        super(MobileFlowForm, self).__init__(*args, **kwargs)

        #----------------------------------------------------------------------
        # get the selected event from the args. If there are no events defined
        # in the database, the value will be None, so set the text to read
        # 'No Events defined'
        #----------------------------------------------------------------------
        flow_name = args[0]['mobile_flow']

        if flow_name is None:
            self.fields['mobile_flow'] = forms.CharField()
            self.fields['mobile_flow'].widget.attrs['readonly'] = True
            self.data['mobile_flow'] = 'No Events defined'
        else:
            self.fields['mobile_flow'] = forms.ChoiceField(label='Mobile Flow',
                                       choices=[ (o.friendly_name, str(o))
                                           for o in MobileFlow.objects.all()])
        self.fields['mobile_flow_count'] = forms.IntegerField(
                                              label='Mobile Flow to Raise',
                                              min_value=1)
        self.fields['mobile_flow_rate'] = forms.FloatField(
                                           label='Mobile Flow Rate (per sec)',
                                           min_value=0.0,
                                           max_value=10.0)
        return

class SyslogForm(forms.Form):
    ''' Syslog  Form

    Allows the user to choose a Syslog Object and how many events to raise
    at a given rate.
    '''

    def __init__(self, *args, **kwargs):
        '''Constructor to allocate dynamic choices.

        The constructor is needed to initialise the Syslog choices so
        it reflects the state of the database at the point of use.
        '''
        super(SyslogForm, self).__init__(*args, **kwargs)

        #----------------------------------------------------------------------
        # get the selected event from the args. If there are no events defined
        # in the database, the value will be None, so set the text to read
        # 'No Events defined'
        #----------------------------------------------------------------------
        syslog_name = args[0]['syslog']

        if syslog_name is None:
            self.fields['syslog'] = forms.CharField()
            self.fields['syslog'].widget.attrs['readonly'] = True
            self.data['syslog'] = 'No Events defined'
        else:
            self.fields['syslog'] = forms.ChoiceField(label='syslog',
                                       choices=[ (o.friendly_name, str(o))
                                           for o in Syslog.objects.all()])

        self.fields['syslog_count'] = forms.IntegerField(
                                                       label='Syslog to Raise',
                                                       min_value=1)
        self.fields['syslog_rate'] = forms.FloatField(
                                                 label='Syslog Rate (per sec)',
                                                 min_value=0.0,
                                                 max_value=10.0)
        return

