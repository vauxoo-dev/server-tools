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

from openerp import api, fields, models


class Webhook(models.TransientModel):
    _name = 'webhook'
    # _auto = False

    # driver_remote_address = fields.char(function='_get_driver_remote_address')

    # request = None
    # driver_remote_address = None
    # driver_remote_address = {method: [addr1, addr2]}
    # driver_remote_address = fields.Selection()

    # def _auto_init(self, cr, context=None):
    #     self.driver_remote_address = {}

    # def __init__(self, pool, cr):
        # import pdb;pdb.set_trace()
    #    init_res = super(Webhook, self).__init__(pool, cr)
    #    self.driver_remote_address = {}
    #    self.request = None
    #    self.BORRAR = 0
    #    return init_res
    @api.model
    def get_driver_remote_address(self):
        return {}

    @api.model
    def get_request_remote_addr(self):
        remote_addr = None
        if True:#try:
            remote_addr = self.request.httprequest.remote_addr
        #except BaseException:
        #    pass
        return remote_addr
    
    # @api.model
    def set_request(self, request):
        self.request = request

    @api.model
    def get_driver_method(self):
        # import pdb;pdb.set_trace()
#        print "*"*100, self.BORRAR
        remote_addr = self.get_request_remote_addr()
        # import pdb;pdb.set_trace()
        for method_name, address_list in self.get_driver_remote_address().iteritems():
            # TODO: Validate list or string
            # for address in address_list:
            #    if remote_addr in ipaddress.ip_network(address):
            #        return method_name
            for address in address_list:
                ipn = ipaddress.ip_network(u'' + address)
                hosts = [host.exploded for host in ipn.hosts()]
                hosts.append(address)
                if remote_addr in hosts:
                    return method_name
            #if remote_addr in address_list:
            #    return method_name
        return False

    @api.model
    def run_webhook(self):
        """
        Method to redirect json request to method to process.
        """
        # from pprint import pprint
        # pprint(request.jsonrequest)
        # print type(request.httprequest.headers)
        # print dir(request.httprequest.headers)
	# import pdb;pdb.set_trace()
        # for att in [att for att in dir(request) if not "__" in att]: print att,":", repr( getattr(request, att) ) 
        method_name = self.get_driver_method()
        if method_name is False:
            return None
        webhook_method = getattr(self, method_name)
        return webhook_method()
