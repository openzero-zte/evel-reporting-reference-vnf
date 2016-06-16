@echo off
REM Initialize the database containing event definitions.  Needed at the start
REM of time or when the application has been upgraded so data migrations need 
REM to be run.

python ..\..\code\webserver\django\manage.py migrate
pause
python ..\..\code\webserver\django\manage.py createsuperuser
pause
