#!/usr/bin/env python
'''
Wraps the API to the OpenStack Nova metadata service.

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

from urllib2 import urlopen, URLError
import logging
import json

logger = logging.getLogger('backend.meta')

class OpenstackMetadataService(object):
    '''
    Class to wrap up the OpenStack metadata service.
    
    Accessing the properties will fetch the metadata, if not already present. 
    '''
    METADATA_URL = 'http://169.254.169.254/openstack/latest/meta_data.json'

    def __init__(self):
        '''
        Constructor - sets internal state to empty/not valid so that first use
        will go and fetch the metadata from the OpenStack metadata service.
        '''
        self.current = False
        self.metadata = {}
        return

    def update(self):
        '''
        Update the metadata from the metadata service.
        
        Note that we need the application to work in non-OpenStack environments
        when testing, so take the view that any failure to access the metadata
        service means we're in a test environment.  This is a bit of a drastic
        assumption and could hide OpenStack networking problems.
        '''
        logger.info('Updating instance metadata from OpenStack')
        try:
            svc = urlopen(OpenstackMetadataService.METADATA_URL,
                          timeout=5)
            logger.debug('URL opened')
            json_metadata = svc.read()
            logger.debug('Retrieved Metadata is: {}'.format(json_metadata))
            self.metadata = json.loads(json_metadata)
            logger.debug('Decoded Metadata is: {}'.format(self.metadata))
            self.current = True

        except URLError:
            #------------------------------------------------------------------
            # Assume that no metadata service means we're in a test environment
            # so fix the data to test values.
            #------------------------------------------------------------------
            logger.warning('Metadata service is not reachable.  '
                           'Assume that we\'re running in a test environment')
            self.metadata['hostname'] = 'Not in OpenStack Environment'
            self.metadata['name'] = 'Not in OpenStack Environment'
            self.metadata['uuid'] = 'Not in OpenStack'
            print('Metadata access failed: assuming test environment')
            self.current = True

        return

    @property
    def hostname(self):
        '''
        Accessor to the hostname.
        
        Using the accessor will trigger access to the metadata service if the
        state of this object is not current.  
        '''
        if (not self.current):
            self.update()
        return self.metadata['hostname']

    @property
    def name(self):
        '''
        Accessor to the VM name.
        
        Using the accessor will trigger access to the metadata service if the
        state of this object is not current.  
        '''
        if (not self.current):
            self.update()
        return self.metadata['name']

    @property
    def uuid(self):
        '''
        Accessor to the VM UUID.
        
        Using the accessor will trigger access to the metadata service if the
        state of this object is not current.  
        '''
        if (not self.current):
            self.update()
        return self.metadata['uuid']
