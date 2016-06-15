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
        self.superfluous_work = 'sale'

    def tearDown(self):
        super(TestSuperfluousDependencies, self).tearDown()
        self.imm.clear_caches()

    def create_module_superfluous_deps(self, superfluous_work):
        """Create a module with superfluous dependencies
        Search a module with dependencies and create a new one adding
        the dependencies and sub-dependencies
        :param superfluous_work str: Name of the module of work to create it
            superfluous in dependencies of new one.
        """
        work_module = self.imm.search([('name', '=', superfluous_work)],
                                      limit=1)
        superfluous_ids = work_module.downstream_dependencies(
            exclude_states=['wo_exc'])
        self.assertTrue(superfluous_ids)
        superfluous = self.imm.browse(superfluous_ids[0])
        new_module_data = {
            'name': work_module.name + '_superfluous',
            'dependencies_id': [
                (0, 0, {'name': work_module.name}),
                (0, 0, {'name': superfluous.name}),
            ]}
        new_module = work_module.copy(new_module_data)
        return new_module

    def test_superfluous_dependencies(self):
        """Test superfluous dependencies
        """
        module = self.create_module_superfluous_deps(self.superfluous_work)
        superfluous_depend_ids = module.compute_superfluous_dependencies()
        self.assertEqual(len(superfluous_depend_ids), 1)
        superfluous = self.imm.browse(superfluous_depend_ids)
        self.assertEqual(superfluous.name, self.superfluous_work)
