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

from openerp.addons.web import http
from openerp.http import request


class WebhookController(http.Controller):

    @http.route('/webhook', type='json', auth='none', method=['POST'])
    def webhook(self, *args, **kwargs):
        '''
        Webhook odoo controller to receive json request and send to
        driver method.
        You will need create your webhook with http://0.0.0.0:0000/webhook
        NOTE: Important use --db-filter params in odoo start.
        '''
        cr, uid = request.cr, request.uid
        request.registry['webhook'].run_webhook(cr, uid, request)
