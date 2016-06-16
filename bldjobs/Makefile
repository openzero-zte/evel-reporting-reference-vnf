#******************************************************************************
# The DCAE Event Reporting Makefile.
#
# Make the various targets associated with housekeeping functions as part of
# Event Reporting Reference VNF.
#
# NOTE: because Makefiles assign special meaning to the TAB character you
#       will need to set tabstops to 2 characters for the layout to look OK.
#
# License
# -------
#
# Copyright(c) <2016>, AT&T Intellectual Property.  All other rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:  This product includes
#    software developed by the AT&T.
# 4. Neither the name of AT&T nor the names of its contributors may be used to
#    endorse or promote products derived from this software without specific
#    prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY AT&T INTELLECTUAL PROPERTY ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL AT&T INTELLECTUAL PROPERTY BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#******************************************************************************

ARCH=$(shell getconf LONG_BIT)
CODE_ROOT=$(CURDIR)/..
WEBSITE_ROOT=$(CODE_ROOT)/code/webserver/django
BACKEND_ROOT=$(CODE_ROOT)/code/backend
COLLECTOR_ROOT=$(CODE_ROOT)/code/collector
LIBS_DIR=$(CODE_ROOT)/libs/x86_$(ARCH)
OUTPUT_DIR=$(CODE_ROOT)/output/x86_$(ARCH)
CONFIG_ROOT=$(CODE_ROOT)/config
DOCS_ROOT=$(CODE_ROOT)/docs
SCP=scp
SSH=ssh
JAVA=java
PLANTUML=/usr/local/bin/plantuml.jar
PLANTFLAGS=-tsvg

#******************************************************************************
# The testbed is a VM instance where we can install the VNF example.          *
#******************************************************************************
VNF_TESTBED=172.18.152.190
COLLECTOR_TESTBED=$(VNF_TESTBED)
VNF_TESTBED_USER=centos
COLLECTOR_TESTBED_USER=centos
TESTBED_WEB_INSTALL_PATH=/opt/att/website
TESTBED_BACKEND_INSTALL_PATH=/opt/att/backend
TESTBED_COLLECTOR_INSTALL_PATH=/opt/att/collector
TESTBED_CONFIG_INSTALL_PATH=/etc/opt/att
TESTBED_SERVICE_INSTALL_PATH=/etc/systemd/system
TESTBED_DOWNLOAD_PATH=./download
TESTBED_LOGFILE_PATH=/var/log/att
TEAM_DOCS_SERVER=covlx8
DOCS_SERVER_PATH=/var/www/html/reporting

#******************************************************************************
# Implicit rule to make diagram files using PlantUML.                         *
#******************************************************************************
%.svg : %.plantuml
	@echo Making $(notdir $@)
	$(JAVA) -jar $(PLANTUML) $(PLANTFLAGS) $<

all:     

clean:   website_clean \
         backend_clean \
         collector_clean
         
install: website_install config_install backend_install collector_install
docs:    docs_clean plantuml_docs sphinx_docs

database_create:
	cd $(WEBSITE_ROOT); python manage.py migrate

#******************************************************************************
# Copy the website onto a testbed server where it can be accessed by clients. *
#******************************************************************************
website_install: website_clean
	@echo Installing website...
	@$(SSH) $(VNF_TESTBED_USER)@$(VNF_TESTBED) \
          rm -rf $(TESTBED_DOWNLOAD_PATH)/\* \; \
          mkdir -p $(TESTBED_DOWNLOAD_PATH)/website
	@$(SCP) -r $(WEBSITE_ROOT)/* \
           $(VNF_TESTBED_USER)@$(VNF_TESTBED):$(TESTBED_DOWNLOAD_PATH)/website
	@$(SSH) -t $(VNF_TESTBED_USER)@$(VNF_TESTBED) \
          sudo cp -r $(TESTBED_DOWNLOAD_PATH)/website/\* \
                     $(TESTBED_WEB_INSTALL_PATH) \; \
          sudo chown -R root:root $(TESTBED_WEB_INSTALL_PATH)
          
  #----------------------------------------------------------------------------
  # Apply the migrations - this leaves a log file owned by centos that we need
  # to blow away so that Apache can write it.  We need the logfile to be 
  # removed before running this target, which is achieved by the website_clean
  # target for us.
  #----------------------------------------------------------------------------
	@echo Applying any new migrations...
	@$(SSH) -t $(VNF_TESTBED_USER)@$(VNF_TESTBED) \
          python $(TESTBED_WEB_INSTALL_PATH)/manage.py migrate \; \
          rm -f $(TESTBED_LOGFILE_PATH)/django.log \; \
          
	@echo Restarting HTTP server...
	@$(SSH) -t $(VNF_TESTBED_USER)@$(VNF_TESTBED) \
          sudo systemctl daemon-reload \; \
          sudo systemctl enable httpd \; \
          sudo systemctl restart httpd

website_clean:
	@echo Cleaning website...
	@$(SSH) -t $(VNF_TESTBED_USER)@$(VNF_TESTBED) \
          sudo rm -rf $(TESTBED_WEB_INSTALL_PATH)/\* \; \
          sudo rm -f $(TESTBED_LOGFILE_PATH)/django.log \; \
          mkdir -p $(TESTBED_WEB_INSTALL_PATH)

#******************************************************************************
# Copy the backend onto a testbed server where it can be accessed by the      *
# the colocated website or remote test clients.                               *
#******************************************************************************
backend_install: backend_clean
	@echo Installing backend...
	@$(SSH) $(VNF_TESTBED_USER)@$(VNF_TESTBED) \
          rm -rf $(TESTBED_DOWNLOAD_PATH)/\* \; \
          mkdir -p $(TESTBED_DOWNLOAD_PATH)/backend
	@$(SCP) -r $(BACKEND_ROOT)/*.py \
           $(VNF_TESTBED_USER)@$(VNF_TESTBED):$(TESTBED_DOWNLOAD_PATH)/backend
	@$(SCP) -r $(CONFIG_ROOT)/backend.service \
             $(VNF_TESTBED_USER)@$(VNF_TESTBED):$(TESTBED_DOWNLOAD_PATH)
	@$(SSH) -t $(VNF_TESTBED_USER)@$(VNF_TESTBED) \
          sudo install -m=644 -t $(TESTBED_BACKEND_INSTALL_PATH) \
                                 $(TESTBED_DOWNLOAD_PATH)/backend/\* 
	@$(SSH) -t $(VNF_TESTBED_USER)@$(VNF_TESTBED) \
          sudo install -m=644 $(TESTBED_DOWNLOAD_PATH)/backend.service \
                              $(TESTBED_SERVICE_INSTALL_PATH)
	@$(SSH) -t $(VNF_TESTBED_USER)@$(VNF_TESTBED) \
          sudo systemctl daemon-reload \; \
          sudo systemctl enable backend \; \
          sudo systemctl restart backend

backend_clean:
	@echo Cleaning backend...
	@$(SSH) -t $(VNF_TESTBED_USER)@$(VNF_TESTBED) \
          sudo rm -rf $(TESTBED_BACKEND_INSTALL_PATH)/\* \
                      $(TESTBED_LOGFILE_PATH)/backend\*

#******************************************************************************
# Copy the "collector" onto a testbed server where it can be accessed by the  *
# backend of the instances of the Reference VNF in the network.               *
#******************************************************************************
collector_install: collector_clean
	@echo Installing collector...
	@$(SSH) $(VNF_TESTBED_USER)@$(VNF_TESTBED) \
          rm -rf $(TESTBED_DOWNLOAD_PATH)/\* \; \
          mkdir -p $(TESTBED_DOWNLOAD_PATH)/collector
	@$(SCP) -r $(COLLECTOR_ROOT)/*.py \
          $(VNF_TESTBED_USER)@$(VNF_TESTBED):$(TESTBED_DOWNLOAD_PATH)/collector
	@$(SSH) -t $(VNF_TESTBED_USER)@$(VNF_TESTBED) \
          sudo install -m=644 -t $(TESTBED_COLLECTOR_INSTALL_PATH) \
                                 $(TESTBED_DOWNLOAD_PATH)/collector/\* 

collector_clean:
	@echo Cleaning collector...
	@$(SSH) -t $(VNF_TESTBED_USER)@$(VNF_TESTBED) \
          sudo rm -rf $(TESTBED_COLLECTOR_INSTALL_PATH)/\* \
                      $(TESTBED_LOGFILE_PATH)/collector\*

#******************************************************************************
# Copy the config files to the relevant locations - expect to be orchestrated *
# endin.                                                                      *
#******************************************************************************
config_install:
	@echo Installing backend config...
	@$(SCP) $(CONFIG_ROOT)/backend.conf \
          $(VNF_TESTBED_USER)@$(VNF_TESTBED):$(TESTBED_CONFIG_INSTALL_PATH)
	@echo Installing collector config...
	@$(SCP) $(CONFIG_ROOT)/collector.conf \
          $(COLLECTOR_TESTBED_USER)@$(COLLECTOR_TESTBED):$(TESTBED_CONFIG_INSTALL_PATH)
	@$(SCP) $(DOCS_ROOT)/att_interface_definition/event_format_updated.json \
          $(COLLECTOR_TESTBED_USER)@$(COLLECTOR_TESTBED):$(TESTBED_CONFIG_INSTALL_PATH)
	@$(SCP) $(DOCS_ROOT)/att_interface_definition/base_schema.json \
          $(COLLECTOR_TESTBED_USER)@$(COLLECTOR_TESTBED):$(TESTBED_CONFIG_INSTALL_PATH)

config_clean:
	@echo Cleaning backend config...
	@$(SSH) $(VNF_TESTBED_USER)@$(VNF_TESTBED) \
          rm -rf $(TESTBED_CONFIG_INSTALL_PATH)/backend.conf
	@echo Cleaning collector config...
	@$(SSH) $(COLLECTOR_TESTBED_USER)@$(COLLECTOR_TESTBED) \
          rm -rf $(TESTBED_CONFIG_INSTALL_PATH)/backend.conf

#******************************************************************************
# Making a clean delivery has some very specific dependencies which are order *
# dependent, so we recursively make a series of targets to do a clean  build  *
# of all of the required deliverables and then finally zipping up.            *
#******************************************************************************
delivery: 
	@$(MAKE) -s delivery_baseline
	@$(MAKE) -s package_all
	@$(MAKE) -s package_collector
	
delivery_baseline:	docs

#******************************************************************************
# Package the software for delivery.                                          *
#******************************************************************************
package_all: 
	@echo Packaging the software for delivery
	@cd $(CODE_ROOT) && tar cfz output/reporting-package.tgz  bldjobs \
																											code \
																											config \
																											docs \
																											hot \
																											scripts \
																											readme.md

package_collector: 
	@echo Packaging the Test Collector software for delivery
	@cd $(CODE_ROOT) && tar cfz output/test-collector-package.tgz \
																											code/collector \
																											config/collector.conf \
																											docs/att_interface_definition \
																											docs/test_collector_user_guide \
																											scripts/linux/go-collector.sh \
																											scripts/windows/go-collector.bat \
																											readme_collector.md

package_clean:
	@echo Clean delivery packages
	@$(RM) $(OUTPUTDIR)/*.tgz

#******************************************************************************
# Create project documentation.                                               *
#******************************************************************************
plantuml_docs: 	$(DOCS_ROOT)/architecture.svg 

sphinx_docs:
	@echo Making Sphinx source code documentation...
	@$(MAKE) -C $(DOCS_ROOT)/code html
	
docs_clean:
	@echo Cleaning docs...
	@$(RM) $(DOCS_ROOT)/*.svg
	@$(RM) -r $(DOCS_ROOT)/code/reporting_build/*
	
docs_install: docs
	$(SCP) -r $(DOCS_ROOT)/code/reporting_build/html/* \
	          root@$(TEAM_DOCS_SERVER):$(DOCS_SERVER_PATH)
