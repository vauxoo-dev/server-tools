# -*- encoding: utf-8 -*-
##############################################################
#    Module Writen For Odoo, Open Source Management Solution
#
#    Copyright (c) 2011 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info Vauxoo (info@vauxoo.com)
#    coded by: moylop260@vauxoo.com
#    planned by: nhomar@vauxoo.com
#                moylop260@vauxoo.com
############################################################################

import ipaddress

from openerp import api, models


class Webhook(models.TransientModel):
    _name = 'webhook'

    @api.one
    def set_event(self):
        self.env.webhook_event = None

    @api.one
    def set_driver_remote_address(self):
        self.env.webhook_driver_address = {}

    @api.one
    def set_driver_name(self):
        # import pdb;pdb.set_trace()
        self.set_driver_remote_address()
        self.env.webhook_driver_name = self.get_driver_name()[0]  # TODO: Why needed [0]
        print "self.env.webhook_driver_name", self.env.webhook_driver_name
    
    @api.one
    def set_remote_address(self):
        self.env.webhook_remote_address = self.env.request.httprequest.remote_addr

    @api.one
    def set_method_event_name(self):
        self.env.method_event_name = None
        if self.env.webhook_driver_name and self.env.webhook_event:
            self.env.method_event_name = \
                'run_webhook_' + self.env.webhook_driver_name + \
                '_' + self.env.webhook_event

    @api.one
    def set_webhook_env(self, request):
        self.env.request = request
        self.set_remote_address()
        self.set_driver_name()
        self.set_event()
        self.set_method_event_name()

    @api.one
    def get_driver_name(self):
        for driver_name, address_list in \
                self.env.webhook_driver_address.iteritems():
            # TODO: Validate list or string
            for address in address_list:
                ipn = ipaddress.ip_network(u'' + address)
                hosts = [host.exploded for host in ipn.hosts()]
                hosts.append(address)
                if self.env.webhook_remote_address in hosts:
                    return driver_name
        return None

    @api.one
    def run_webhook(self):
        """
        Method to redirect json request to method to process.
        """
        print "self.env.webhook_driver_name", self.env.webhook_driver_name
        print "self.env.method_event_name", self.env.method_event_name
        #import pdb;pdb.set_trace()
        if self.env.webhook_driver_name is None \
                or self.env.method_event_name is None \
                or not hasattr(self, self.env.method_event_name):
            # TODO: Add exception odoo
            return None
        # TODO: validate is don't exists attr
        webhook_method = getattr(self, self.env.method_event_name)
        return webhook_method()
