# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
import logging

from openerp.tests import common

_logger = logging.getLogger(__name__)
MODULE = os.path.basename(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class TestModelsInheritedTransientModel(common.TransactionCase):
    """Check if a models is inherited for TransientModel for a Model
    """

    def setUp(self):
        super(TestModelsInheritedTransientModel, self).setUp()
        self.imm = self.env['ir.module.module']
        self.work_module = 'document'

    def tearDown(self):
        super(TestModelsInheritedTransientModel, self).tearDown()
        self.imm.clear_caches()

    def test_models_inherited_transient_model(self):
        """Test if a models is inherited for TransientModel for a Model"""
        import pdb
        pdb.set_trace()
