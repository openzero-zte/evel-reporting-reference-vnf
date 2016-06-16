@echo off
REM Run the event management service responsible for sending events to the 
REM backend collector.

python ..\..\code\backend\backend.py ^
       --config ..\..\config\backend.conf ^
       --section windows ^
       --verbose
