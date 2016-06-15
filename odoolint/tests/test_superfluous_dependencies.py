# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
import logging

from openerp.tests import common

_logger = logging.getLogger(__name__)
MODULE = os.path.basename(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class TestSuperfluousDependencies(common.TransactionCase):
    """Test superfluous dependencies
    """

    def setUp(self):
        super(TestSuperfluousDependencies, self).setUp()
        self.imm = self.env['ir.module.module']

    def tearDown(self):
        super(TestSuperfluousDependencies, self).tearDown()
        self.imm.clear_caches()

    def create_module_superfluous_deps(self):
        new_module = self.imm.search([('name', '=', MODULE)], limit=1).copy({
            'name': MODULE + '_copy'})
        import pdb;pdb.set_trace()
        return new_module

    def test_superfluous_dependencies(self):
        module = self.create_module_superfluous_deps()
        module.name
