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

class GithubWebhook(models.Model):
    _name = 'github.webhook'
    _auto = False

    @api.one
    def run_hook(self, request):
        from pprint import pprint
        pprint(request.jsonrequest)
        print type(request.httprequest.headers)
        print dir(request.httprequest.headers)
        authorization, repo_id = self.auth_token(self.cr, self.uid, [1], self.request)
        print authorization, repo_id
        pprint('Here is the json, ')
        return True
