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

from openerp import models, fields, api

class Webhook(models.Model):
    _name = 'webhook'
    _auto = False

    @api.model
    def run_hook(self, request):
	"""
	Method to redirect json request to method to process.
	"""
        from pprint import pprint
        pprint(request.jsonrequest)
        #print type(request.httprequest.headers)
        #print dir(request.httprequest.headers)
        #authorization, repo_id = self.auth_token(self.cr, self.uid, [1], self.request)
        #print authorization, repo_id
        #pprint('Here is the json, ')
        return True
