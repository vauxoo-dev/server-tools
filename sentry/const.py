# Copyright 2016-2017 Versada <https://versada.eu/>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

import odoo.loglevels


def split_multiple(string, delimiter=',', strip_chars=None):
    """Splits :param:`string` and strips :param:`strip_chars` from values."""
    if not string:
        return []
    return [v.strip(strip_chars) for v in string.split(delimiter)]


# Mapping of Odoo logging level -> Python stdlib logging library log level.
LOG_LEVEL_MAP = dict([
    (getattr(odoo.loglevels, 'LOG_%s' % x), getattr(logging, x))
    for x in ('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET')
])

DEFAULT_LOG_LEVEL = 'warn'

ODOO_USER_EXCEPTIONS = [
    'odoo.exceptions.AccessDenied',
    'odoo.exceptions.AccessError',
    'odoo.exceptions.DeferredException',
    'odoo.exceptions.MissingError',
    'odoo.exceptions.RedirectWarning',
    'odoo.exceptions.UserError',
    'odoo.exceptions.ValidationError',
    'odoo.exceptions.Warning',
    'odoo.exceptions.except_orm',
]
DEFAULT_IGNORED_EXCEPTIONS = ','.join(ODOO_USER_EXCEPTIONS)

EXCLUDE_LOGGERS = (
    'werkzeug',
)
DEFAULT_EXCLUDE_LOGGERS = ','.join(EXCLUDE_LOGGERS)

DEFAULT_ENVIRONMENT = 'develop'
