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

import logging
import openerp
from openerp.addons.web import http
from openerp.http import request, Response, WebRequest

class Github(http.Controller):

    @http.route('/github', type='json', auth='none', method=['POST'])
    def github_hook(self, *args, **kwargs):
        '''
        Github hook odoo controller to receive json from github and send to
	driver method.
	You will need create your webhook with http://0.0.0.0:0000/github
	NOTE: Important use --db-filter params in odoo start.
        '''
	cr, uid = request.cr, request.uid
        request.registry['github.webhook'].run_hook(cr, uid, request)
