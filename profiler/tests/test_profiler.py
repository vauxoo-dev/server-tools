# coding: utf-8
# License AGPL-3 or later (http://www.gnu.org/licenses/lgpl).
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>

from odoo import tests


@tests.at_install(False)
@tests.post_install(True)
class TestProfiler(tests.HttpCase):

    def test_profiler_tour(self):
        self.phantom_js('/',
                        "odoo.__DEBUG__.services['web.Tour'].run('profile')",
                        "odoo.__DEBUG__.services['web.Tour'].tours.profile",
                        login='admin')
