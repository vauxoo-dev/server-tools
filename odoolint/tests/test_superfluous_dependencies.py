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
        """Create a module with superfluous dependencies
        Search a module with dependencies and create a new one adding
        the dependencies and sub-dependencies
        """
        current_module = self.imm.search([('name', '=', MODULE)], limit=1)
        new_deps = self.imm.search([
            ('dependencies_id', '!=', False),
            ('dependencies_id.name', '!=', 'base'),
        ], limit=2)
        new_sub_dep_names = list(set(new_deps.mapped(
            'dependencies_id.depend_id.dependencies_id.name')) |
            set(new_deps.mapped('name')))
        depends_o2m_data = []
        for new_sub_dep_name in new_sub_dep_names:
            depends_o2m_data.append((0, 0, {'name': new_sub_dep_name}))
        new_module_data = {
            'name': MODULE + '_copy',
            'dependencies_id': depends_o2m_data,
        }
        new_module = current_module.copy(new_module_data)
        return new_module

    def test_superfluous_dependencies(self):
        """Test superfluous dependencies
        """
        module = self.create_module_superfluous_deps()
        superfluous_depend_ids = module.compute_superfluous_dependencies()
        self.assertTrue(superfluous_depend_ids)
