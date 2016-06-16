#!/usr/bin/env python
'''
Test framework for AT&T's Vendor Event Listener Reference VNF.

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

import unittest
import traceback
import sys
import os
import signal
from multiprocessing import Process
import time
import socket
import json

from event import Event
import collector
import backend


def go_process(test_name, process_name, entry_point):
    ''' Start a sub-process for the system under test.
    
    This function will be called from a new process and is responsible for
    invoking the entry-point function.  It overrides the system argv so that
    the process can be invoked as if from the command-line.  It overrides
    stdout and stderr so that we can capture the output for diagnostics in 
    unique files.
    '''
    print('Starting {} process for {}'.format(process_name, test_name))

    try:
        stdout_filename = 'log/{}-{}-stdout.log'.format(test_name,
                                                        process_name)
        stderr_filename = 'log/{}-{}-stderr.log'.format(test_name,
                                                        process_name)
        syslog_filename = 'log/{}.log'.format(process_name)
        syslog_unique_filename = 'log/{}-{}-syslog.log'.format(test_name,
                                                               process_name)

        #----------------------------------------------------------------------
        # Make sure that all of the log files are removed.
        #----------------------------------------------------------------------
        for fname in [stdout_filename,
                      stderr_filename,
                      syslog_filename,
                      syslog_unique_filename]:
            if (os.path.exists(fname)):
                os.unlink(fname)

        #----------------------------------------------------------------------
        # Override the argv and stdout/stderr for the process before invoking
        # the main entry point for the backend.
        #----------------------------------------------------------------------
        sys.argv = ['{}-{}'.format(process_name, test_name),
                    '--verbose',
                    '--config', './config/system_test_{}.conf'.format(
                                                                 process_name)]
        sys.stdout = open(stdout_filename, 'w', 0)
        sys.stderr = open(stderr_filename, 'w', 0)
        entry_point()

    except Exception as e:
        #----------------------------------------------------------------------
        # If we hit an exception capture it into stderr (remembering we've
        # hooked that into a file) and then re-throw the exception.
        #----------------------------------------------------------------------
        sys.stderr.write('{} threw exception: {}\n'.format(process_name, e))
        exception_info = sys.exc_info()
        traceback.print_tb(exception_info[2])
        raise e

    return

class SystemTestCase(unittest.TestCase):
    MAX_STARTUP_TIME = 5
    STARTUP_RETRY_INTERVAL = 0.5

    def setUp(self):
        print(79 * '-')
        print('Setup {}'.format(self._testMethodName))
        self.children_running = False
        self.collector = Process(target=go_process,
                                 args=(self._testMethodName,
                                       'collector',
                                       collector.main))
        self.collector.start()
        self.backend = Process(target=go_process,
                                 args=(self._testMethodName,
                                       'backend',
                                       backend.main))
        self.backend.start()

        #----------------------------------------------------------------------
        # In order to synchronize with the backend, wait for it to accept
        # commands successfully.  Limit how many attempts so that catastrophic
        # failures don't cause the tests to hang indefinitely.
        #----------------------------------------------------------------------
        retries = 0
        command = {'action': 'ping'}
        while (self.children_running == False and
               retries < SystemTestCase.MAX_STARTUP_TIME / SystemTestCase.STARTUP_RETRY_INTERVAL):
            try:
                self.send_command(command)
                print('Backend process is up ({})'.format(retries))
                self.children_running = True

            except Exception as e:
                retries += 1
                time.sleep(SystemTestCase.STARTUP_RETRY_INTERVAL)

    def tearDown(self):
        self.stop_child_processes()
        return

    def wait_stable(self, expected_duration=0.0):
        ''' Wait for the test to run to completion.
        
        In the absence of anything smarter, we wait for the expected run 
        duration plus a small safety margin.
        '''
        time.sleep(expected_duration + 1.0)
        return

    def send_command(self, cmd):
        ''' Send a command to the system under test.
        
        This can throw lots of exceptions, which should all be treated as test 
        failures so don't handle them locally.
        '''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 27000))
        s.sendall(json.dumps(cmd))
        s.close()
        return

    def stop_child_processes(self):
        ''' Stop the processes under test.
        
        Stops the processes under test, if and only if they're currently 
        running.  This makes stopping multiple times safe.  We need this 
        behaviour because some tests require that we stop the processes to 
        assess the results, but we want the generic teardown to clean-up if
        the processes are still running.
        '''

        print('Stopping processes:')
        if (self.children_running):
            try:
                os.kill(self.collector.pid, signal.SIGINT)
                print('   Collector stopped')
            except Exception as e:
                print('   Kill Collector Exception {} '.format(e))
            try:
                os.kill(self.backend.pid, signal.SIGINT)
                print('   Backend stopped')
            except Exception as e:
                print('   Kill Backend Exception {} '.format(e))
            self.backend.join(1)
            self.collector.join(1)
            self.children_running = False


            #------------------------------------------------------------------
            # Rename the syslog files so we keep them for each test.
            #------------------------------------------------------------------
            os.rename('log/backend.log',
                      'log/{}-backend-syslog.log'.format(self._testMethodName))
            os.rename('log/collector.log',
                      'log/{}-collector-syslog.log'.format(
                                                         self._testMethodName))

        else:
            print('   Already stopped')

        return

    def read_logs(self):
        ''' Read all the log-files we expect from the child processes.
        
        Enables the tests to check that contents are as expected.
        '''
        self.backend_syslog = open('log/{}-{}-syslog.log'.format(
                                                         self._testMethodName,
                                                         'backend')).read()
        self.backend_stdout = open('log/{}-{}-stdout.log'.format(
                                                         self._testMethodName,
                                                         'backend')).read()
        self.backend_stderr = open('log/{}-{}-stderr.log'.format(
                                                         self._testMethodName,
                                                         'backend')).read()
        self.collector_syslog = open('log/{}-{}-syslog.log'.format(
                                                         self._testMethodName,
                                                         'collector')).read()
        self.collector_stdout = open('log/{}-{}-stdout.log'.format(
                                                         self._testMethodName,
                                                         'collector')).read()
        self.collector_stderr = open('log/{}-{}-stderr.log'.format(
                                                         self._testMethodName,
                                                         'collector')).read()

        #----------------------------------------------------------------------
        # The syslog files can contain "normal" warnings in a test environment.
        # Replace so assertions are OK.
        #----------------------------------------------------------------------
        self.backend_syslog = self.backend_syslog.replace(
                        'WARNING - Metadata service is not reachable',
                        'EXPECTEDWARNING - Metadata service is not reachable')
        return

    def collector_good_responses(self):
        return self.collector_stderr.count('HTTP/1.1" 204')

    def collector_good_authentications(self):
        return self.collector_syslog.count('Authenticated OK')

    def backend_good_responses(self):
        return self.backend_syslog.count('backend.em - DEBUG - Good response')

    def collector_schema_checks_ok(self):
        return self.collector_stdout.count(
                              'Valid body decoded & checked against schema OK')

    def assert_normal_logs(self):
        ''' Check that the log files are as expected.
        
        Contains checks which should be true for the vast majority of tests.
        '''
        self.assertEqual(len(self.backend_stderr), 0,
                         'Unexpected Backend stderr output')
        self.assertGreater(len(self.backend_syslog), 0,
                           'Backend syslog output missing')
        self.assertGreater(len(self.collector_syslog), 0,
                           'Collector syslog output missing')
        self.assertNotIn(' - WARNING - ',
                         self.collector_syslog,
                         'Collector syslog contains WARNING entries')
        self.assertNotIn(' - ERROR - ',
                         self.collector_syslog,
                         'Collector syslog contains ERROR entries')
        self.assertNotIn(' - WARNING - ',
                         self.backend_syslog,
                         'Backend syslog contains WARNING entries')
        self.assertNotIn(' - ERROR - ',
                         self.backend_syslog,
                         'Backend syslog contains ERROR entries')
        return

    def assert_good_responses(self, count):
        self.assertEqual(self.collector_good_responses(),
                         count,
                         'Unexpected number of good responses from collector. '
                         'Expected: {}  Got: {}'.format(count,
                                              self.collector_good_responses()))
        self.assertEqual(self.collector_schema_checks_ok(),
                         count,
                         'Unexpected number of good schema checks.  '
                         'Expected: {}  Got: {}'.format(count,
                                            self.collector_schema_checks_ok()))
        self.assertEqual(self.collector_good_authentications(),
                         count,
                         'Unexpected number of successful authentications.  '
                         'Expected: {}  Got: {}'.format(count,
                                        self.collector_good_authentications()))
        self.assertEqual(self.backend_good_responses(),
                         count,
                         'Unexpected number of good responses from backend.  '
                         'Expected: {}  Got: {}'.format(count,
                                              self.backend_good_responses()))
        return

