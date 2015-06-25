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

from openerp import api, models


class Webhook(models.Model):
    _inherit = 'webhook'

    @api.model
    def get_driver_remote_address(self):
        driver_remote_address = super(
            Webhook, self).get_driver_remote_address()
        driver_remote_address['run_webhook_github'] = ['192.30.252.0/22']
        return driver_remote_address

    @api.one
    def run_webhook_github(self):
        return True
