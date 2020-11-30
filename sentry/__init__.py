# Copyright 2016-2017 Versada <https://versada.eu/>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

import odoo.http
from odoo.service import wsgi_server
from odoo.tools import config as odoo_config

from . import const
from .logutils import SanitizeOdooCookiesProcessor, fetch_git_sha
from .logutils import InvalidGitRepository, get_extra_context

import collections

_logger = logging.getLogger(__name__)
HAS_SENTRY_SDK = True
try:
    import sentry_sdk
    from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware
    from sentry_sdk.integrations.threading import ThreadingIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration, ignore_logger
    from sentry_sdk import HttpTransport
except ImportError:
    HAS_SENTRY_SDK = False
    _logger.debug('Cannot import "sentry-sdk". Please make sure it is installed.')


def before_send(event, hint):
    cxtest = get_extra_context(odoo.http.request)
    
    tags_info = event.setdefault("tags", {})
    tags_info.update(cxtest.setdefault("tags", {}))
    
    user_info = event.setdefault("user", {})
    user_info.update(cxtest.setdefault("user", {}))

    extra_info = event.setdefault('extra', {})
    extra_info.update(cxtest.setdefault('extra', {}))

    request_info = event.setdefault('request', {})
    request_info.update(cxtest.setdefault('request', {}))

    raven_processor = SanitizeOdooCookiesProcessor()
    raven_processor.process(event)

    return event

def get_odoo_commit(odoo_dir):
    """Attempts to get Odoo git commit from :param:`odoo_dir`."""
    if not odoo_dir:
        return
    try:
        return fetch_git_sha(odoo_dir)
    except InvalidGitRepository:
        _logger.debug(
            'Odoo directory: "%s" not a valid git repository', odoo_dir)


def initialize_sentry(config):
    """  Setup an instance of :class:`sentry_sdk.Client`.
        :param config: Sentry configuration
        :param client: class used to instantiate the sentry_sdk client.
    """
    enabled = config.get('sentry_enabled', False)
    if not (HAS_SENTRY_SDK and enabled):
        return

    if config.get('sentry_odoo_dir') and config.get('sentry_release'):
        _logger.debug('Both sentry_odoo_dir and sentry_release defined, choosing sentry_release')

    release = config.get('sentry_release', get_odoo_commit(config.get('sentry_odoo_dir')))

    level = config.get('sentry_logging_level', const.DEFAULT_LOG_LEVEL)
    exclude_loggers = const.split_multiple(
        config.get('sentry_exclude_loggers', const.DEFAULT_EXCLUDE_LOGGERS)
    )

    exclude_exceptions = const.split_multiple(
        config.get('sentry_exclude_exceptions', const.DEFAULT_IGNORED_EXCEPTIONS)
    )

    if level not in const.LOG_LEVEL_MAP:
        level = const.DEFAULT_LOG_LEVEL

    sentry_logging = LoggingIntegration(
        level=const.LOG_LEVEL_MAP[level],
        event_level=logging.WARNING
    )

    client = sentry_sdk.init(
        dsn= config.get('sentry_dsn'),
        environment=config.get('sentry_environment', const.DEFAULT_ENVIRONMENT),
        release=release,
        integrations=[sentry_logging,
                      ThreadingIntegration(propagate_hub=True)],
        transport=HttpTransport,
        before_send=before_send,
    )

    if exclude_loggers:
        for item in exclude_loggers:
            ignore_logger(item)

    if exclude_exceptions:
        for item in exclude_exceptions:
            ignore_logger(item)

    wsgi_server.application = SentryWsgiMiddleware(wsgi_server.application)

    with sentry_sdk.push_scope() as scope:
        scope.set_extra('debug', False)
        sentry_sdk.capture_message('Starting Odoo Server', 'info')

    return client


def post_load():
    _logger.info("Initializing sentry...")
    initialize_sentry(odoo_config)
