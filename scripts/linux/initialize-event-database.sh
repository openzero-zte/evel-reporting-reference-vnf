# Initialize the database containing event definitions.  Needed at the start
# of time or when the application has been upgraded so data migrations need 
# to be run.

python ../../code/webserver/django/manage.py migrate
python ../../code/webserver/django/manage.py createsuperuser

