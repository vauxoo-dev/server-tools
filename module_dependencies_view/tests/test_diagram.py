# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger
from odoo import http
from mock import patch, Mock

from ..controllers.main import ModuleDependenciesView


class TestDiagram(TransactionCase):
    def setUp(self):
        super(TestDiagram, self).setUp()

        self.module = self.env['ir.module.module'].search(
            [('name', '=', 'account')])
        self.mock_http()

    def mock_http(self):
        """Method used to mock the connection with
        the controllers and receives the data used to render them
        allowing us to verify that it is correct
        """
        self.patcher = patch('odoo.http.route', lambda **kwargs: True)
        self.patcher.start()
        self.http_request_orig = http.request
        http.request = Mock(lambda **kwargs: True)
        http.request.cr = self.cr
        http.request.uid = self.uid
        http.request.env = self.env
        http.request.httprequest = Mock(lambda **kwargs: True)
        http.request.context = {}
        http.request.session = Mock()
        http.request.session.uid = 1
        http.request.render = lambda template, qcontext:\
            {'template_id': template, 'qcontext': qcontext}

    @mute_logger('odoo.http')
    def test_10_dependencies_one_leve(self):
        """ Test for the dependency modules in one level"""
        dependencies = ModuleDependenciesView()
        res = dependencies.module_level(self.module)
        self.assertEqual(res['template_id'],
                         "module_dependencies_view.module")
        module = res['qcontext']['object']
        self.assertEqual(self.module, module)

    @mute_logger('odoo.http')
    def test_20_dependencies(self):
        """ Test for the dependency modules in tree view"""
        dependencies = ModuleDependenciesView()
        res = dependencies.module(self.module)
        self.assertEqual(res['template_id'],
                         "module_dependencies_view.module")
        module = res['qcontext']['object']
        self.assertEqual(self.module, module)

    def tearDown(self):
        self.patcher.stop()
        http.request = self.http_request_orig
        super(TestDiagram, self).tearDown()
