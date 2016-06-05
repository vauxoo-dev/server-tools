# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os

from openerp.tests import common
from openerp import tools


class TestConvertFile(common.TransactionCase):
    """Test convert_file method patched
    """

    def setUp(self):
        super(TestConvertFile, self).setUp()
        self.imd = self.env['ir.model.data']
        self.imd_old = self.imd.search([])
        self.module = os.path.basename(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        self.fdemo = 'demo/partner_category_demo.xml'
        self.fdata = 'data/partner_category_data.xml'
        self.fdata2 = 'data/partner_category_data2.xml'
        self.cr._serialized = False
        self.cr.autocommit(False)
        print id(self.cr), id(self.env.cr)

    def clear_caches(self):
        self.imd_diff = (self.imd.search([]) - self.imd_old)
        for imd_diff in self.imd_diff:
            imd_diff_old_api = self.registry['ir.model.data'].browse(
                self.cr, self.uid, imd_diff.id)
            imd_diff.clear_caches()
            imd_diff_old_api.clear_caches()
            # imd_diff_old_api.xmlid_lookup.clear_cache(imd_diff_old_api)
        self.registry['ir.model.data'].clear_caches()
        self.imd.clear_caches()
        # self.imd.xmlid_lookup.clear_cache(self.imd)
        # self.imd_diff.xmlid_lookup.clear_cache(self.imd_diff)


    def tearDown(self):
        self.clear_caches()
        super(TestConvertFile, self).tearDown()
        self.clear_caches()

    def _load(self, module, fname):
        kind = os.path.dirname(fname)
        tools.convert_file(self.cr, module, fname, {}, 'init',
                           False, kind, self.registry._assertion_report)

    def test_10(self):
        self._load(self.module, self.fdemo)
        self._load(self.module, self.fdata)

    def test_20(self):
        self._load(self.module, self.fdemo)
        self.clear_caches()
        new_imd = self.env['ir.model.data'].search([
            ('module', '=', self.module), ('file_name', '=', self.fdemo)])
        print "*"*100, new_imd.id, new_imd.name, new_imd.model, new_imd.res_id
        print "record", self.env[new_imd.model].browse(new_imd.res_id).name
        # import pdb;pdb.set_trace()
        self._load(self.module, self.fdata)
        # self._load(self.module, self.fdata2)

        # self._load(self.module, 'data', self.fdata)
    # model_name = 'res.partner.category'

    # def setUp(self):
    #     super(TestConvertFile, self).setUp()
    #     # self.registry('ir.model.data').clear_caches()
    #     # self.env['ir.model.data'].clear_caches()
    #     self.module = os.path.basename(
    #         os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    #     self.fdemo = 'demo/partner_category_demo.xml'
    #     self.fdata = 'data/partner_category_data.xml'
    #     self.fdata2 = 'data/partner_category_data2.xml'
    #     # self.cr._serialized = False
    #     # self.cr.autocommit(False)
    #     # self.model_data_old = self.env['ir.model.data'].search([])

    # # def tearDown(self):
    # #     # openerp.api.Environment.reset()
    # #     self.model_data_new = self.env['ir.model.data'].search([])
    # #     (self.model_data_new - self.model_data_old).unlink()
    # #     super(TestConvertFile, self).tearDown()

    # def test_20_demo_ref_from_data(self):
    #     """Test demo referenced from data
    #     """
    #     # _, model, res_id = self.env['ir.model.data'].xmlid_lookup(self.module + '.' + 'res_partner_category_demo_01')
    #     # model_obj_b = self.env[model].browse(res_id)
    #     convert_file(self.cr, self.module, self.fdemo, None, kind='demo')
    #     # _, model, res_id = self.env['ir.model.data'].xmlid_lookup(self.module + '.' + 'res_partner_category_demo_01')
    #     # model_obj_a = self.env[model].browse(res_id)
    #     # print model_obj_a.name
    #     convert_file(self.cr, self.module, self.fdata, None, kind='data')

    # def test_10_demo_overwritten_from_data(self):
    #     """Test demo overwritten from data
    #     """
    #     convert_file(self.cr, self.module, self.fdemo, None, kind='demo')
    #     convert_file(self.cr, self.module, self.fdata, None, kind='data')
    #     # convert_file(self.cr, self.module, self.fdata2, None, kind='data')
