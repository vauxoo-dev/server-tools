# coding: utf-8
# © 2015 Vauxoo - http://www.vauxoo.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# info Vauxoo (info@vauxoo.com)
# coded by: nhomar@vauxoo.com
# planned by: nhomar@vauxoo.com

import subprocess

from openerp import models
from openerp.tools.translate import _


class Module(models.Model):
    _inherit = 'ir.module.module'

    def get_info(self, _path):
        label = {}
        try:
            label['sha'] = subprocess.check_output([
                "git", "describe", "--always", "--dirty"], cwd=_path)
            label['status'] = '<br/>'.join(subprocess.check_output([
                "git", "status"], cwd=_path).split('\n'))
            label['remotes'] = subprocess.check_output([
                "git", "remote", "-v"], cwd=_path).split('\n')
        except Exception:
            label['sha'] = _('Not a valid git repository')
            label['status'] = _('No valid information')
            label['remotes'] = _('No valid information')
        return label