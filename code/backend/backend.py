#!/usr/bin/env python
'''
Program which acts as the backend for the web front-end, accepting commands
which then result in actions to raise events (faults and measurements) to send 
across the Vendor Event Listener API.

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

from command_handler import start_server
from time import sleep
from event_manager import create_event_manager

import sys
import os
import platform
import traceback
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import ConfigParser
import logging.handlers

__all__ = []
__version__ = 0.1
__date__ = '2015-12-04'
__updated__ = '2015-12-04'

TESTRUN = False
DEBUG = False
PROFILE = False

event_manager = None


def main(argv=None):
    '''
    Main function for the daemon start-up.
    
    Called with command-line arguments:
        *    --config *<file>*
        *    --section *<section>*
        *    --verbose 
        
    Where:
    
        *<file>* specifies the path to the configuration file.
        
        *<section>* specifies the section within that config file.
        
        *verbose* generates more information in the log files.
        
    The process may be run as a daemon or as a foreground process and listens
    for commands from the web-server front-end.  Each command typically results
    in a worker-thread being created to handle generation of the requested
    events.
    '''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = 'v{}'.format(__version__)
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s {} ({})'.format(program_version,
                                                         program_build_date)
    if (__import__('__main__').__doc__ is not None):
        program_shortdesc = __import__('__main__').__doc__.split('\n')[1]
    else:
        program_shortdesc = 'Running in test harness'
    program_license = '''{}

  Created  on {}.
  Copyright 2015 Metaswitch Networks Ltd. All rights reserved.

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
'''.format(program_shortdesc, str(__date__))

    try:
        #----------------------------------------------------------------------
        # Setup argument parser so we can parse the command-line.
        #----------------------------------------------------------------------
        parser = ArgumentParser(description=program_license,
                                formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument('-v', '--verbose',
                            dest='verbose',
                            action='count',
                            help='set verbosity level')
        parser.add_argument('-V', '--version',
                            action='version',
                            version=program_version_message,
                            help='Display version information')
        parser.add_argument('-c', '--config',
                            dest='config',
                            default='/etc/opt/att/backend.conf',
                            help='Use this config file.',
                            metavar='<file>')
        parser.add_argument('-s', '--section',
                            dest='section',
                            default='default',
                            metavar='<section>',
                            help='section to use in the config file')

        #----------------------------------------------------------------------
        # Process arguments received.
        #----------------------------------------------------------------------
        args = parser.parse_args()
        verbose = args.verbose
        config_file = args.config
        config_section = args.section

        #----------------------------------------------------------------------
        # Now read the config file, using command-line supplied values as
        # overrides.
        #----------------------------------------------------------------------
        defaults = {'log_file': 'backend.log',
                    'port': '27115',
                    'vel_domain': '',
                    'vel_port': '12233',
                    'vel_path': '',
                    'vel_topic_name': '',
                    'vel_use_https': 'Yes',
                    'heartbeat_interval': '60'
                   }
        overrides = {}
        config = ConfigParser.SafeConfigParser(defaults)
        print('Config file: {}'.format(config_file))
        config.read(config_file)

        #----------------------------------------------------------------------
        # extract the values we want.
        #----------------------------------------------------------------------
        log_file = config.get(config_section, 'log_file', vars=overrides)
        server_port = int(config.get(config_section, 'port', vars=overrides))
        vel_domain = config.get(config_section, 'vel_domain', vars=overrides)
        vel_port = int(config.get(config_section, 'vel_port', vars=overrides))
        vel_path = config.get(config_section, 'vel_path', vars=overrides)
        vel_username = config.get(config_section,
                                  'vel_username',
                                  vars=overrides)
        vel_password = config.get(config_section,
                                  'vel_password',
                                  vars=overrides)
        vel_topic_name = config.get(config_section,
                                    'vel_topic_name',
                                    vars=overrides)
        vel_use_https = config.get(config_section,
                                   'vel_use_https',
                                   vars=overrides).lower() in ['yes', 'true']
        heartbeat_interval = int(config.get(config_section,
                                        'heartbeat_interval',
                                        vars=overrides))

        #----------------------------------------------------------------------
        # Finally we have enough info to start a proper flow trace.
        #----------------------------------------------------------------------
        logger = logging.getLogger('backend')
        if verbose > 0:
            print('Verbose mode on')
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        handler = logging.handlers.RotatingFileHandler(log_file,
                                                       maxBytes=1000000,
                                                       backupCount=10)
        if (platform.system() == 'Windows'):
            date_format = '%Y-%m-%d %H:%M:%S'
        else:
            date_format = '%Y-%m-%d %H:%M:%S.%f %z'
        formatter = logging.Formatter('%(asctime)s %(name)s - '
                                      '%(levelname)s - %(message)s',
                                      date_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.info('Started')

        #----------------------------------------------------------------------
        # Log the details of the configuration.
        #----------------------------------------------------------------------
        logger.debug('Log file = {}'.format(log_file))
        logger.debug('Server Port = {}'.format(server_port))
        logger.debug('Event Listener Domain = {}'.format(vel_domain))
        logger.debug('Event Listener Port = {}'.format(vel_port))
        logger.debug('Event Listener Path = {}'.format(vel_path))
        logger.debug('Event Listener Username = {}'.format(vel_username))
        # logger.debug('Event Listener Password = {}'.format(vel_password))
        logger.debug('Event Listener Topic = {}'.format(vel_topic_name))
        logger.debug('Event Listener HTTPS = {}'.format(vel_use_https))
        logger.debug('Heartbeat Interval = {}'.format(heartbeat_interval))

        #----------------------------------------------------------------------
        # Perform some basic error checking on the config.
        #----------------------------------------------------------------------
        if (int(server_port) < 1024 or int(server_port) > 65535):
            logger.error('Invalid server port ({}) specified'.format(
                                                                 server_port))
            raise RuntimeError('Invalid server port ({}) specified'.format(
                                                                 server_port))

        if (int(vel_port) < 1 or int(vel_port) > 65535):
            logger.error('Invalid Vendor Event Listener port ({}) '
                         'specified'.format(vel_port))
            raise RuntimeError('Invalid Vendor Event Listener port ({}) '
                               'specified'.format(vel_port))

        if (len(vel_path) > 0 and vel_path[-1] != '/'):
            logger.warning('Event Listener Path ({}) should have terminating '
                           '"/"!  Adding one on to configured string.'.format(
                                                                     vel_path))
            vel_path += '/'

        #----------------------------------------------------------------------
        # We are now ready to get started with processing. Start-up the various
        # components of the system in order:
        #
        #  1) The EventManager which acts as the factory for new events and
        #     which maintains a queue of events to be sent to the collector.
        #  2) The server listening on the TCP socket for new commands.
        #----------------------------------------------------------------------
        event_manager = create_event_manager(vel_domain,
                                     int(vel_port),
                                     vel_path,
                                     vel_username,
                                     vel_password,
                                     vel_topic_name,
                                     vel_use_https)
        logger.debug('Foreground event manager created')
        event_manager.start()
        print('Hostname: {}'.format(event_manager.vm_name))
        print(' VM UUID: {}'.format(event_manager.vm_id))
        start_server(int(server_port))

        #----------------------------------------------------------------------
        # The backend mainloop wakes up every second and is responsible for:
        #
        #  1) Generating periodic heartbeats at the configured rate.
        #  2) Managing the simulation of the orderly shutdown.
        #----------------------------------------------------------------------
        time_to_heartbeat = 0
        while True:
            #==================================================================
            # Check whether a heartbeat is due.  Note that we arrange to send
            # one immediately we enter the main-loop so the collector knows
            # we're awake.
            #==================================================================
            if (time_to_heartbeat == 0):
                logger.info('Sending heartbeat. Next in {} secs'.format(
                                                           heartbeat_interval))
                event = event_manager.new_heartbeat()
                event_manager.post_event(event)
                time_to_heartbeat = heartbeat_interval
            time_to_heartbeat -= 1

            #==================================================================
            # Give the Event Manager the opportunity to manage VNF state
            # transitions
            #==================================================================
            event_manager.update_vnf_state()

            #==================================================================
            # Mainloop sleep.
            #==================================================================
            sleep(1)

        logger.error('Main loop exited unexpectedly!')
        return 0

    except KeyboardInterrupt:
        #----------------------------------------------------------------------
        # handle keyboard interrupt
        #----------------------------------------------------------------------
        logger.info('Exiting on keyboard interrupt!')
        return 0

    except Exception as e:
        #----------------------------------------------------------------------
        # Handle unexpected exceptions.
        #----------------------------------------------------------------------
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * ' '
        sys.stderr.write(program_name + ': ' + repr(e) + '\n')
        sys.stderr.write(indent + '  for help use --help\n')
        sys.stderr.write(traceback.format_exc())
        logger.critical('Exiting because of exception: {}'.format(e))
        logger.critical(traceback.format_exc())
        return 2

#------------------------------------------------------------------------------
# MAIN SCRIPT ENTRY POINT.
#------------------------------------------------------------------------------
if __name__ == '__main__':
    if TESTRUN:
        #----------------------------------------------------------------------
        # Running tests - note that doctest comments haven't been included so
        # this is a hook for future improvements.
        #----------------------------------------------------------------------
        import doctest
        doctest.testmod()

    if PROFILE:
        #----------------------------------------------------------------------
        # Profiling performance.  Performance isn't expected to be a major
        # issue, but this should all work as expected.
        #----------------------------------------------------------------------
        import cProfile
        import pstats
        profile_filename = 'backend_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open('backend_profile_stats.txt', 'wb')
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)

    #--------------------------------------------------------------------------
    # Normal operation - call through to the main function.
    #--------------------------------------------------------------------------
    sys.exit(main())
