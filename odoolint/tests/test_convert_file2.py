# # -*- coding: utf-8 -*-
# # © 2016  Vauxoo (<http://www.vauxoo.com/>)
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# import os

# from openerp.tests import common
# from openerp import tools


# class TestConvertFile(common.TransactionCase):
#     """Test convert_file method patched
#     """

#     def setUp(self):
#         super(TestConvertFile, self).setUp()
#         self.module = os.path.basename(
#             os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#         self.fdemo = 'demo/partner_category_demo.xml'
#         self.fdata = 'data/partner_category_data.xml'
#         self.fdata2 = 'data/partner_category_data2.xml'

#     def tearDown(self):
#         self.registry['ir.model.data'].clear_caches()
#         self.registry['res.partner.category'].clear_caches()

#     def _load(self, module, fname):
#         kind = os.path.dirname(fname)
#         tools.convert_file(self.cr, self.module, fname, {}, 'init',
#                            False, kind, self.registry._assertion_report)

#     def test_20(self):
#         self._load(self.module, self.fdemo)
#         self._load(self.module, self.fdata2)

#         # self._load(self.module, 'data', self.fdata)
