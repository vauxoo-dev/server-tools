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

from openerp import api, exceptions, fields, models, tools
from openerp.tools.translate import _


class WebhookAddress(models.Model):
    _name = 'webhook.address'

    name = fields.Char(
        'IP or Network Address',
        required=True,
        help='IP or network address of your consumer webhook:\n'
        'ip address e.g.: 10.10.0.8\n'
        'network address e.g. of: 10.10.0.8/24',
    )
    webhook_id = fields.Many2one(
        'webhook', 'Webhook', required=True, ondelete='cascade')


class Webhook(models.Model):
    _name = 'webhook'

    name = fields.Char('Consumer name',
        required=True,
        help='Name of your consumer webhook.'
        'This name will be used in named of event methods')
    address_ids = fields.One2many(
        'webhook.address', 'webhook_id', 'IP or Network Address',
        required=True,
        help='This address will be filter to know who is '
        'consumer webhook')
    python_code_get_event = fields.Text(
        'Get event',
        required=True,
        help='Python code to get event from request data.\n'
        'You have object.env.request variable with full '
        'webhook request.',
        default='# You can use object.env.request variable '
        'to get full data of webhook request.\n'
        '# Example:\n#object.env.request.httprequest.'
        'headers.get("X-Github-Event")',
    )
    python_code_get_ip = fields.Text(
        'Get IP',
        required=True,
        help='Python code to get remote IP address '
        'from request data.\n'
        'You have object.env.request variable with full '
        'webhook request.',
        default='# You can use object.env.request variable '
        'to get full data of webhook request.\n'
        '# Example:\n#object.env.request.httprequest.remote_addr'
        '\nobject.env.request.httprequest.remote_addr',

    )
    active = fields.Boolean(default=True)

    @api.one
    def process_python_code(self, python_code, request=None):
        res = None
        try:
            res = eval(
                python_code,
                {'user': self.env.user,
                 'object': self,
                 'request': request,
                 # copy context to prevent side-effects of eval
                 'context': dict(self.env.context),
            })
        except:
            # TODO: add debug log
            print "eval error", python_code
        if isinstance(res, basestring):
            res = tools.ustr(res)
        return res

    @api.model
    def search_with_request(self, request):
        """
        Method to search of all webhook
        and return only one that match with remote address
        and range of address.
        """
        for webhook in self.search([('active', '=', True)]):
            remote_address = webhook.process_python_code(
                webhook.python_code_get_ip, request)[0]
            if not remote_address:
                continue
            import pdb;pdb.set_trace()
            if webhook.is_address_range(remote_address)[0]:
                return webhook
        return False

    @api.one
    def is_address_range(self, remote_address):
        for address in self.address_ids:
            ipn = ipaddress.ip_network(u'' + address.name)
            hosts = [host.exploded for host in ipn.hosts()]
            hosts.append(address.name)
            if remote_address in hosts:
                return True
        return False

    @api.one
    def run_webhook(self, request):
        event = self.process_python_code(
            self.python_code_get_event, request)[0]
        if not event:
            raise exceptions.ValidationError(_(
                'event is not defined'))
        method_event_name = \
            'run_webhook_' + self.name + \
            '_' + event
        if not hasattr(self, method_event_name):
            raise exceptions.ValidationError(_(
                'Not defined method "%s" yet' % (
                    method_event_name)))
        method = getattr(self, method_event_name)
        res_method = method()[0]
        if res_method is NotImplemented:
            raise exceptions.ValidationError(_(
                'Not implemented method "%s" yet' % (
                    method_event_name)))
        return res_method

