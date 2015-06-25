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

    @api.model
    def get_driver_remote_address(self):
        return {}

    @api.model
    def get_request_remote_addr(self):
        remote_addr = None
        remote_addr = self.request.httprequest.remote_addr
        return remote_addr

    def set_request(self, request):
        self.request = request

    @api.model
    def get_driver_method(self):
        remote_addr = self.get_request_remote_addr()
        for method_name, address_list in \
                self.get_driver_remote_address().iteritems():
            # TODO: Validate list or string
            for address in address_list:
                ipn = ipaddress.ip_network(u'' + address)
                hosts = [host.exploded for host in ipn.hosts()]
                hosts.append(address)
                if remote_addr in hosts:
                    return method_name
        return False

    @api.model
    def run_webhook(self):
        """
        Method to redirect json request to method to process.
        """
        method_name = self.get_driver_method()
        if method_name is False:
            return None
        webhook_method = getattr(self, method_name)
        return webhook_method()
