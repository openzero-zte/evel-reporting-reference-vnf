from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^faults/$', views.raise_fault, name='faults'),
    url(r'^measurements/$', views.raise_measurement, name='measurements'),
    url(r'^mobile_flow/$', views.raise_mobile_flow, name='mobile_flow'),
    url(r'^syslog/$', views.raise_syslog, name='syslog'),
    url(r'^lifecycle/$', views.lifecycle, name='lifecycle'),
    url(r'^clear_event_counter/$', views.clear_event_counter, name='clear_event_counter'),
    url(r'^faults/thanks/$', views.posted, name='fault_posted'),
    url(r'^faults/failed/$', views.failed, name='fault_failed'),
    url(r'^mobile_flow/thanks/$', views.posted, name='fault_posted'),
    url(r'^mobile_flow/failed/$', views.failed, name='fault_failed'),
    url(r'^syslog/thanks/$', views.posted, name='fault_posted'),
    url(r'^syslog/failed/$', views.failed, name='fault_failed'),
    url(r'^measurements/thanks/$', views.posted, name='fault_posted'),
    url(r'^measurements/failed/$', views.failed, name='fault_failed'),
    url(r'^lifecycle/thanks/$', views.posted, name='lifecycle_posted'),
    url(r'^lifecycle/failed/$', views.failed, name='lifecycle_failed'),
]