# coding: utf-8
# License AGPL-3 or later (http://www.gnu.org/licenses/lgpl).
# Copyright 2014 Anybox <http://anybox.fr>
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>

# import urllib

from openerp import tests


@tests.at_install(False)
@tests.post_install(True)
class TestProfiler(tests.HttpCase):
    # def test_profiler(self):
    #     self.base_url = self.env['ir.config_parameter'].get_param('web.base.url')
    #     self.authenticate('admin', 'admin')
    #     data = urllib.urlencode({})
    #     response = self.url_open(self.base_url + "/web/profiler/enable", data)
    #     # response = self.url_open(self.base_url + "/web/profiler/disable")
    #     import pdb
    #     pdb.set_trace()
    #     response = self.url_open(self.base_url + "/web/profiler/dump")

    def test_profiler_tour(self):
        self.phantom_js('/', "openerp.Tour.run('profile_run', 'test')",
                        'openerp.Tour.tours.profile_run', login='admin')
