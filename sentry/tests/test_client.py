# Copyright 2016-2017 Versada <https://versada.eu/>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import sys
from odoo.tests import TransactionCase
from odoo.tools import config, mute_logger

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from odoo import exceptions

from .. import initialize_sentry
# from ..logutils import OdooSentryHandler
from sentry_sdk.client import Client
from sentry_sdk.hub import Hub, _InitGuard


class CustomLoggingIntegration(LoggingIntegration):
    pass

class InMemoryClient(Client):
    '''A :class:`sentry.Client` subclass which simply stores events in a list.

    Extended based on the one found in sentry-python to avoid additional testing
    dependencies: https://git.io/vyGO3
    '''

    def __init__(self, **kwargs):
        self.events = []
        super(InMemoryClient, self).__init__(**kwargs)

    def is_enabled(self):
        return True

    def capture_event(self, event, *args, **kwargs):
        self.events.append(event)

    # def send(self, **kwargs):
    #     import pdb;pdb.set_trace()
    #     self.events.append(kwargs)

    def has_event(self, event_level, event_msg):
        for event in self.events:
            if (event.get('level') == event_level and
                    event.get('logentry', {}).get('message') == event_msg):
                return True
        return False

def initialize_sentry_memory(*args, **kwargs):
    # type: (*Optional[str], **Any) -> ContextManager[Any]
    """Initializes the SDK and optionally integrations.

    This takes the same arguments as the client constructor.
    """
    client = InMemoryClient(*args, **kwargs)  # type: ignore
    Hub.current.bind_client(client)
    rv = _InitGuard(client)
    return rv


class TestClientSetup(TransactionCase):
    def setUp(self):
        super(TestClientSetup, self).setUp()
        self.logger = logging.getLogger(__name__)
        self.dsn = 'http://public:secret@example.com/1'
        config = {
            'sentry_enabled': True,
            'sentry_dsn': self.dsn,
        }
        self.client = initialize_sentry(
            config, client_meth=initialize_sentry_memory)._client
        # self.client.integrations['logging'] = CustomLoggingIntegration()
        # self.client.integrations['logging']._handler
        # self.client.integrations['logging']._breadcrumb_handler


    def assertEventCaptured(self, client, event_level, event_msg):
        self.assertTrue(
            client.has_event(event_level, event_msg),
            msg='Event: "%s" was not captured' % event_msg
        )

    def test_initialize_sentry_sets_dsn(self):
        """Check if the sentry_dsn is taken from conf custom"""
        self.assertEqual(self.client.dsn, self.dsn)

    def test_capture_event(self):
        level, msg = logging.WARNING, 'Test event, can be ignored'
        # import pdb;pdb.set_trace()
        # with mute_logger(__name__):
        self.logger.log(level, msg)
        # print(logger.handlers)
        level = "\x1b[1;33m\x1b[1;49mwarning\x1b[0m"
        self.assertEventCaptured(self.client, level, msg)


# def log_handler_by_class(logger, handler_cls):
#     for handler in logger.handlers:
#         if isinstance(handler, handler_cls):
#             yield handler


# def remove_logging_handler(logger_name, handler_cls):
#     '''Removes handlers of specified classes from a :class:`logging.Logger`
#     with a given name.

#     :param string logger_name: name of the logger

#     :param handler_cls: class of the handler to remove. You can pass a tuple of
#         classes to catch several classes
#     '''
#     logger = logging.getLogger(logger_name)
#     for handler in log_handler_by_class(logger, handler_cls):
#         logger.removeHandler(handler)

# class InMemoryClient(sentry_sdk.Client):
#     '''A :class:`sentry.Client` subclass which simply stores events in a list.

#     Extended based on the one found in sentry-python to avoid additional testing
#     dependencies: https://git.io/vyGO3
#     '''

#     def __init__(self, **kwargs):
#         self.events = []
#         super(InMemoryClient, self).__init__(**kwargs)

#     def is_enabled(self):
#         return True

#     def send(self, **kwargs):
#         self.events.append(kwargs)

#     def has_event(self, event_level, event_msg):
#         for event in self.events:
#             if (event.get('level') == event_level and
#                     event.get('message') == event_msg):
#                 return True
#         return False


# def initialize_sentry_memory(*args, **kwargs):
#     # type: (*Optional[str], **Any) -> ContextManager[Any]
#     """Initializes the SDK and optionally integrations.

#     This takes the same arguments as the client constructor.
#     """
#     client = InMemoryClient(*args, **kwargs)  # type: ignore
#     Hub.current.bind_client(client)
#     rv = _InitGuard(client)
#     return rv

# class TestClientSetup(TransactionCase):

#     def setUp(self):
#         super(TestClientSetup, self).setUp()
#         self.logger = logging.getLogger(__name__)

#         # Sentry is enabled by default, so the default handler will be added
#         # when the module is loaded. After that, subsequent calls to
#         # setup_logging will not re-add our handler. We explicitly remove
#         # OdooSentryHandler handler so we can test with our in-memory client.
#         remove_logging_handler('', OdooSentryHandler)

#     def assertEventCaptured(self, client, event_level, event_msg):
#         self.assertTrue(
#             client.has_event(event_level, event_msg),
#             msg='Event: "%s" was not captured' % event_msg
#         )

#     def assertEventNotCaptured(self, client, event_level, event_msg):
#         self.assertFalse(
#             client.has_event(event_level, event_msg),
#             msg='Event: "%s" was captured' % event_msg
#         )

#     def test_initialize_sentry_sets_dsn(self):
#         config = {
#             'sentry_enabled': True,
#             'sentry_dsn': 'http://public:secret@example.com/1',
#         }
#         client = initialize_sentry(config, client_meth=initialize_sentry_memory)
#         self.assertEqual(client.remote.base_url, 'http://example.com')

#     def test_capture_event(self):
#         config = {
#             'sentry_enabled': True,
#             'sentry_dsn': 'http://public:secret@example.com/1',
#         }
#         level, msg = logging.WARNING, 'Test event, can be ignored'
#         client = initialize_sentry(config, client_cls=InMemoryClient)
#         self.logger.log(level, msg)
#         self.assertEventCaptured(client, level, msg)

#     def test_ignore_exceptions(self):
#         config = {
#             'sentry_enabled': True,
#             'sentry_dsn': 'http://public:secret@example.com/1',
#             'sentry_ignore_exceptions': 'odoo.exceptions.UserError',
#         }
#         level, msg = logging.WARNING, 'Test UserError'
#         client = initialize_sentry(config, client_cls=InMemoryClient)

#         handlers = list(
#             log_handler_by_class(logging.getLogger(), OdooSentryHandler)
#         )
#         self.assertTrue(handlers)
#         handler = handlers[0]
#         try:
#             raise exceptions.UserError(msg)
#         except exceptions.UserError:
#             exc_info = sys.exc_info()
#         record = logging.LogRecord(
#             __name__, level, __file__, 42, msg, (), exc_info)
#         handler.emit(record)
#         self.assertEventNotCaptured(client, level, msg)
