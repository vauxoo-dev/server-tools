# -*- coding: utf-8 -*-
##############################################################
#    Module Writen For Odoo, Open Source Management Solution
#
#    Copyright (c) 2011 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    license: http://www.gnu.org/licenses/agpl-3.0.html
#    info Vauxoo (info@vauxoo.com)
#    coded by: moylop260@vauxoo.com
#    planned by: nhomar@vauxoo.com
#                moylop260@vauxoo.com
############################################################################

import logging
import traceback

import ipaddress

from openerp import api, exceptions, fields, models, tools
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


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

    name = fields.Char(
        'Consumer name',
        required=True,
        help='Name of your consumer webhook. '
             'This name will be used in named of event methods')
    # NOT IMPLEMENTED YET
    ip_validation_ok = fields.Boolean(
	help='IP security validation. If is True then '
	     'will check that remote IP is in range of address.'
    )
    address_ids = fields.One2many(
        'webhook.address', 'webhook_id', 'IP or Network Address',
        required=True,
        help='This address will be filter to know who is '
             'consumer webhook.')
    # NOT IMPLEMENTED YET
    secret = fields.Boolean(
	help='String secret similar to one password to validate '
	     'consumer webhook.'
    )
    ping_event = fields.Char(
	help='Name of event ping.\nIt is a dummy event '
	     'just to know if a provider is working.',
	default='ping',
    )
    python_code_get_event = fields.Text(
        'Get event',
        required=True,
        help='Python code to get event from request data.\n'
             'You have object.env.request variable with full '
             'webhook request.',
        default='# You can use object.env.request variable '
                'to get full data of webhook request.\n'
                '# Example:\n#request.httprequest.'
                'headers.get("X-Github-Event")',
    )
    python_code_get_ip = fields.Text(
        'Get IP',
        required=True,
        help='Python code to get remote IP address '
             'from request data.\n'
             'You have "request" variable with full '
             'webhook request.',
        default='# You can use "request" variable '
                'to get full data of webhook request.\n'
                '# Example:\n'
                '#object.env.request.httprequest.remote_addr'
                '\nrequest.httprequest.remote_addr',

    )
    active = fields.Boolean(default=True)
    #TODO: Add a o2m function to show all server actions
    #TODO: Add a function to show all methods

    @api.one
    def process_python_code(self, python_code, request=None):
        """
        Execute a python code with eval.
        :param string python_code: Python code to process
        :param object request: Request object with data of json
                               and http request
        :return: Result of process python code.
        """
        res = None
        eval_dict = {
            'user': self.env.user,
            'object': self,
            'request': request,
            # copy context to prevent side-effects of eval
            'context': dict(self.env.context),
        }
        try:
            # pylint: disable=W0123
            res = eval(
                python_code,
                eval_dict,
            )
        except BaseException:
            error = tools.ustr(traceback.format_exc())
            _logger.debug(
                'python_code "%s" with dict [%s] error [%s]',
                python_code, eval_dict, error)
        if isinstance(res, basestring):
            res = tools.ustr(res)
        return res

    @api.one
    def is_address_range(self, remote_address):
        """
        Check if a remote IP address is in range of one
        IP or network address of current object data.
        :param string remote_address: Remote IP address
        :return: if remote address match then return True
                 else then return False
        """
        for address in self.address_ids:
            ipn = ipaddress.ip_network(u'' + address.name)
            hosts = [host.exploded for host in ipn.hosts()]
            hosts.append(address.name)
            if remote_address in hosts:
                return True
        return False

    @api.model
    def get_event_methods(self, event_method_base):
        """
        List all methods for this webhook object
	that start with base name.
        e.g. if exists methods called 'x1', 'x2'
        and other ones called 'y1', 'y2'
        if you have event_method_base='x'
        Then will return ['x1', 'x2']
        :param string event_method_base: Name of method event base
        returns: List of methods start with method base
        """
        return sorted(
            attr for attr in dir(self) if attr.startswith(
                event_method_base) and callable(getattr(self, attr))
        )

    @api.model
    def get_server_actions(self, event_method_base):
	"""
	List all code servers actions
	for webhook model
	that start with base name.
	e.g. if exist servers action called 'x1', 'x2'
	and other ones called 'y1', 'y2'
	if you have event_method_base='x'
	then will return ['x1', 'x2']
	:param string event_method_base: Name of method event base
	returns: List of server actions objects start wtih method base
	"""
	return self.env['ir.actions.server'].search([
	    ('name', 'like', event_method_base + '%'),
	    ('state', '=', 'code'),
	    ('model_id.model', '=', 'webhook'),
	])

    @api.one
    def run_webhook(self, request):
        """
        Run methods to process a webhook event.
        Get all methods with base name
        'run_CONSUMER_EVENT*'
        Invoke all methods found.
        :param object request: Request object with data of json
                               and http request
        :return: True
        """
        event = self.process_python_code(
            self.python_code_get_event, request)[0]
        if not event:
            raise exceptions.ValidationError(_(
                'event is not defined'))
    	if event == self.ping_event:
            # if is a 'ping' event then return True
            # because the request is received fine.
	    return True
        method_event_name_base = \
            'run_' + self.name + \
            '_' + event
        self.env.request = request
        for method_event_name in self.get_event_methods(
	    method_event_name_base):
            method = getattr(self, method_event_name)
            res_method = method()
            if isinstance(res_method, list) and len(
		res_method) == 1:
                if res_method[0] is NotImplemented:
                    _logger.debug(
                        'Not implemented method "%s" yet',
			method_event_name)
	self.get_server_actions(method_event_name_base).run()
        return True
