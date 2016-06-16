Web Server
===========

The web-server is written using the Django framework. Refer to the Django 
documentation for details.  The key aspects of the usage are highlighted here,
but overall the application is a "plain-vanilla" example of a Django 
application.


Application
-----------
There is a single Django application :py:mod:`reporting_app` which implements
the models and views required for the Vendor Event Listener Reference VNF 
application.

Data Model
----------

There are three key models:

  1)  Faults
    
  2)  Measurements
    
  3)  Application Config
    
The Faults and Measurements model the relevant information in the API for the 
two event types with the common information in the Event header being 
duplicated between the two.

The Application Config is currently unused. 

Views
-----

The following views are provided:

  * Index

    The web application is accessed by HTTP at::

        http://<INSTANCE_IP>/
        
    To allow for future expansion, this redirects to:: 
    
        http://<INSTANCE_IP>/reporting/ 

    Provides a "landing-page" to navigate to the other views.
        
  * Administration View

    The administration views are all located under::

        http://<INSTANCE_IP>/admin/
    
    The administration pages allow the user to add/modify definitions of 
    Faults and Measurements.

  * Fault Generation

    The Fault generation view is located at::
    
        http://<INSTANCE_IP>/faults/
        
    The view allows the user to generate one or more Faults at a defined rate.
    
  * Measurement Generation
  
    The Measurement generation view is located at::

        http://<INSTANCE_IP>/reporting/measurements/
        
    The view allows the user to generate one or more Measurements at a defined 
    rate.
    
  *  Lifecycle Management

     The Lifecycle Management view is located at::
     
        http://<INSTANCE_IP>/reporting/lifecycle/
        
     The Lifecycle Management page allows the user to trigger the Reference VNF
     to transition through the state **Preparing to Terminate** to 
     **Ready to Terminate** and then back again to **Active**.




