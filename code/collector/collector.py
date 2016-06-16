#!/usr/bin/env python
'''
Program which acts as the collector for the Vendor Event Listener REST API.

Only intended for test purposes.

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

from rest_dispatcher import PathDispatcher, set_404_content
from wsgiref.simple_server import make_server
import sys
import os
import platform
import traceback
import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import ConfigParser
import logging.handlers
from base64 import b64decode
import string
import json
import jsonschema

_hello_resp = '''\
<html>
  <head>
     <title>Hello {name}</title>
   </head>
   <body>
     <h1>Hello {name}!</h1>
   </body>
</html>'''

_localtime_resp = '''\
<?xml version="1.0"?>
<time>
  <year>{t.tm_year}</year>
  <month>{t.tm_mon}</month>
  <day>{t.tm_mday}</day>
  <hour>{t.tm_hour}</hour>
  <minute>{t.tm_min}</minute>
  <second>{t.tm_sec}</second>
</time>'''

__all__ = []
__version__ = 0.1
__date__ = '2015-12-04'
__updated__ = '2015-12-04'

API_VERSION = 1

TESTRUN = False
DEBUG = False
PROFILE = False

#------------------------------------------------------------------------------
# Credentials we expect clients to authenticate themselves with.
#------------------------------------------------------------------------------
vel_username = ''
vel_password = ''

#------------------------------------------------------------------------------
# The JSON schema which we will use to validate.
#------------------------------------------------------------------------------
vel_schema = None

#------------------------------------------------------------------------------
# Logger for this module.
#------------------------------------------------------------------------------
logger = None

def vendor_event_listener(environ, start_response):
    '''
    Handler for the Vendor Event Listener REST API.
    
    Extract headers and the body and check that:
    
      1)  The client authenticated themselves correctly.
      
      2)  The body validates against the schema for the API.
    '''
    logger.info('Got a Vendor Event request')
    print('==== ' + time.asctime() + ' ' + '=' * 49)

    #--------------------------------------------------------------------------
    # Extract the content from the request.
    #--------------------------------------------------------------------------
    length = int(environ.get('CONTENT_LENGTH', '0'))
    logger.debug('Content Length: {0}'.format(length))
    body = environ['wsgi.input'].read(length)
    logger.debug('Content Body: {0}'.format(body))

    mode, b64_credentials = string.split(environ.get('HTTP_AUTHORIZATION',
                                                     'None None'))
    # logger.debug('Auth. Mode: {0} Credentials: {1}'.format(mode,
    #                                                     b64_credentials))
    logger.debug('Auth. Mode: {0} Credentials: ****'.format(mode))
    if (b64_credentials != 'None'):
        credentials = b64decode(b64_credentials)
    else:
        credentials = None

    # logger.debug('Credentials: {0}'.format(credentials))
    logger.debug('Credentials: ****')

    #--------------------------------------------------------------------------
    # If we have a schema file then check that the event matches that expected.
    #--------------------------------------------------------------------------
    if (vel_schema is not None):
        logger.debug('Attempting to validate data: {0}\n'
                     'Against schema: {1}'.format(body, vel_schema))
        try:
            decoded_body = json.loads(body)
            jsonschema.validate(decoded_body, vel_schema)
            logger.info('Event is valid!')
            print('Valid body decoded & checked against schema OK:\n'
                  '{0}'.format(json.dumps(decoded_body,
                                         sort_keys=True,
                                         indent=4,
                                         separators=(',', ': '))))

        except jsonschema.SchemaError as e:
            logger.error('Schema is not valid! {0}'.format(e))
            print('Schema is not valid! {0}'.format(e))

        except jsonschema.ValidationError as e:
            logger.warn('Event is not valid against schema! {0}'.format(e))
            print('Event is not valid against schema! {0}'.format(e))
            print('Bad JSON body decoded:\n'
                  '{0}'.format(json.dumps(decoded_body,
                                         sort_keys=True,
                                         indent=4,
                                         separators=(',', ': '))))

        except Exception as e:
            logger.error('Event invalid for unexpected reason! {0}'.format(e))
            print('Schema is not valid for unexpected reason! {0}'.format(e))
    else:
        logger.debug('No schema so just decode JSON: {0}'.format(body))
        try:
            decoded_body = json.loads(body)
            print('Valid JSON body (no schema checking) decoded:\n'
                  '{0}'.format(json.dumps(decoded_body,
                                         sort_keys=True,
                                         indent=4,
                                         separators=(',', ': '))))
            logger.info('Event is valid JSON but not checked against schema!')

        except Exception as e:
            logger.error('Event invalid for unexpected reason! {0}'.format(e))
            print('JSON body is not valid for unexpected reason! {0}'.format(e))

    #--------------------------------------------------------------------------
    # See whether the user authenticated themselves correctly.
    #--------------------------------------------------------------------------
    if (credentials == (vel_username + ':' + vel_password)):
        logger.debug('Authenticated OK')
        print('Authenticated OK')

        #----------------------------------------------------------------------
        # Respond to the caller.
        #----------------------------------------------------------------------
        start_response('204 No Content', [])
        yield ''
    else:
        logger.warn('Failed to authenticate OK')
        print('Failed to authenticate OK')

        #----------------------------------------------------------------------
        # Respond to the caller.
        #----------------------------------------------------------------------
        start_response('401 Unauthorized', [ ('Content-type',
                                              'application/json')])
        req_error = { 'requestError': {
                        'policyException': {
                            'messageId': 'POL0001',
                            'text': 'Failed to authenticate'
                            }
                        }
                    }
        yield json.dumps(req_error)

def main(argv=None):
    '''
    Main function for the collector start-up.
    
    Called with command-line arguments:
        *    --config *<file>*
        *    --section *<section>*
        *    --verbose 
        
    Where:
    
        *<file>* specifies the path to the configuration file.
        
        *<section>* specifies the section within that config file.
        
        *verbose* generates more information in the log files.
        
    The process listens for REST API invocations and checks them. Errors are
    displayed to stdout and logged.
    '''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = 'v{0}'.format(__version__)
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s {0} ({1})'.format(program_version,
                                                         program_build_date)
    if (__import__('__main__').__doc__ is not None):
        program_shortdesc = __import__('__main__').__doc__.split('\n')[1]
    else:
        program_shortdesc = 'Running in test harness'
    program_license = '''{0}

  Created  on {1}.
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
                            default='/etc/opt/att/collector.conf',
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
        defaults = {'log_file': 'collector.log',
                    'vel_port': '12233',
                    'vel_path': '',
                    'vel_topic_name': ''
                   }
        overrides = {}
        config = ConfigParser.SafeConfigParser(defaults)
        config.read(config_file)

        #----------------------------------------------------------------------
        # extract the values we want.
        #----------------------------------------------------------------------
        log_file = config.get(config_section, 'log_file', vars=overrides)
        vel_port = config.get(config_section, 'vel_port', vars=overrides)
        vel_path = config.get(config_section, 'vel_path', vars=overrides)
        vel_topic_name = config.get(config_section,
                                    'vel_topic_name',
                                    vars=overrides)
        global vel_username
        global vel_password
        vel_username = config.get(config_section,
                                  'vel_username',
                                  vars=overrides)
        vel_password = config.get(config_section,
                                  'vel_password',
                                  vars=overrides)
        vel_schema_file = config.get(config_section,
                                     'schema_file',
                                     vars=overrides)
        base_schema_file = config.get(config_section,
                                 'base_schema_file',
                                  vars=overrides)

        #----------------------------------------------------------------------
        # Finally we have enough info to start a proper flow trace.
        #----------------------------------------------------------------------
        global logger
        print('Logfile: {0}'.format(log_file))
        logger = logging.getLogger('collector')
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
        logger.debug('Log file = {0}'.format(log_file))
        logger.debug('Event Listener Port = {0}'.format(vel_port))
        logger.debug('Event Listener Path = {0}'.format(vel_path))
        logger.debug('Event Listener Topic = {0}'.format(vel_topic_name))
        logger.debug('Event Listener Username = {0}'.format(vel_username))
        # logger.debug('Event Listener Password = {0}'.format(vel_password))
        logger.debug('Event Listener JSON Schema File = {0}'.format(
                                                              vel_schema_file))
        logger.debug('Base JSON Schema File = {0}'.format(base_schema_file))

        #----------------------------------------------------------------------
        # Perform some basic error checking on the config.
        #----------------------------------------------------------------------
        if (int(vel_port) < 1024 or int(vel_port) > 65535):
            logger.error('Invalid Vendor Event Listener port ({0}) '
                         'specified'.format(vel_port))
            raise RuntimeError('Invalid Vendor Event Listener port ({0}) '
                               'specified'.format(vel_port))

        if (len(vel_path) > 0 and vel_path[-1] != '/'):
            logger.warning('Event Listener Path ({0}) should have terminating '
                           '"/"!  Adding one on to configured string.'.format(
                                                                     vel_path))
            vel_path += '/'

        #----------------------------------------------------------------------
        # Load up the vel_schema and base_schema, if they exist.
        #----------------------------------------------------------------------
        if (os.path.exists(vel_schema_file)):
            global vel_schema
            vel_schema = json.load(open(vel_schema_file, 'r'))
            logger.debug('Loaded the JSON schema file')
            if (os.path.exists(base_schema_file)):
                logger.debug('Updating the schema with base definition')
                base_schema = json.load(open(base_schema_file, 'r'))
                vel_schema.update(base_schema)
                logger.debug('Updated the JSON schema file')
        else:
            logger.warning('Event Listener Schema File ({0}) not found. '
                           'No validation will be undertaken.'.format(
                                                              vel_schema_file))

        #----------------------------------------------------------------------
        # We are now ready to get started with processing. Start-up the various
        # components of the system in order:
        #
        #  1) Create the dispatcher.
        #  2) Register the functions for the URLs of interest.
        #  3) Run the webserver.
        #----------------------------------------------------------------------
        root_url = '/{0}eventListener/v{1}{2}'.format(vel_path,
                                                   API_VERSION,
                                                   '/' + vel_topic_name
                                                     if len(vel_topic_name) > 0
                                                     else '')
        set_404_content(root_url)
        dispatcher = PathDispatcher()
        dispatcher.register('GET', root_url, vendor_event_listener)
        dispatcher.register('POST', root_url, vendor_event_listener)
        httpd = make_server('', int(vel_port), dispatcher)
        print('Serving on port {0}...'.format(vel_port))
        httpd.serve_forever()

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
        logger.critical('Exiting because of exception: {0}'.format(e))
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
        profile_filename = 'collector_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open('collector_profile_stats.txt', 'wb')
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)

    #--------------------------------------------------------------------------
    # Normal operation - call through to the main function.
    #--------------------------------------------------------------------------
    sys.exit(main())
