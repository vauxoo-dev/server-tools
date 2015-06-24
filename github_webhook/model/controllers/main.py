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
        Github hook
        '''
        return request.registry['github.webhook'].run_hook(request.cr, request.uid, request)
