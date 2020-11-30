""" Custom class of raven.core.processors taken of https://git.io/JITko
    This is a custom class of processor to filter and sanitize
    passwords and keys from request data, it does not exist in
    sentry-sdk.
"""

from __future__ import absolute_import

import re
import warnings

from sentry_sdk._compat import text_type, PY2

try:
    from collections.abc import Mapping
except ImportError:
    # Python < 3.3
    from collections import Mapping


def string_types():
    """ Taken from https://git.io/JIv5J """

    return str,


def is_namedtuple(value):
    """ https://stackoverflow.com/a/2166841/1843746
        But modified to handle subclasses of namedtuples.
    """
    if not isinstance(value, tuple):
        return False
    f = getattr(type(value), '_fields', None)
    if not isinstance(f, tuple):
        return False
    return all(type(n) == str for n in f)


def iteritems(d, **kw):
    """ Override iteritems for support multiple versions python.
        Taken from https://git.io/JIvMi
    """
    if PY2:
        return d.iteritems(**kw)
    else:
        return iter(d.items(**kw))


def varmap(func, var, context=None, name=None):
    """ Executes ``func(key_name, value)`` on all values
        recurisively discovering dict and list scoped
        values. Taken from https://git.io/JIvMN
    """
    if context is None:
        context = {}
    objid = id(var)
    if objid in context:
        return func(name, '<...>')
    context[objid] = 1

    if isinstance(var, (list, tuple)) and not is_namedtuple(var):
        ret = [varmap(func, f, context, name) for f in var]
    else:
        ret = func(name, var)
        if isinstance(ret, Mapping):
            ret = dict((k, varmap(func, v, context, k))
                       for k, v in iteritems(var))
    del context[objid]
    return ret


class SanitizeKeysProcessor(object):
    """ Class from raven for sanitize keys, cookies, etc
        Asterisk out things that correspond to a configurable set of keys. """

    MASK = '*' * 8

    def process(self, data, **kwargs):
        if 'exception' in data:
            if 'values' in data['exception']:
                for value in data['exception'].get('values', []):
                    if 'stacktrace' in value:
                        self.filter_stacktrace(value['stacktrace'])

        if 'request' in data:
            self.filter_http(data['request'])

        if 'extra' in data:
            data['extra'] = self.filter_extra(data['extra'])

        if 'level' in data:
            data['level'] = self.filter_level(data['level'])

        return data

    @property
    def sanitize_keys(self):
        pass

    def sanitize(self, item, value):
        if value is None:
            return

        if not item:  # key can be a NoneType
            return value

        # Just in case we have bytes here, we want to make them into text
        # properly without failing so we can perform our check.
        if isinstance(item, bytes):
            item = item.decode('utf-8', 'replace')
        else:
            item = text_type(item)

        item = item.lower()
        for key in self.sanitize_keys:
            if key in item:
                # store mask as a fixed length for security
                return self.MASK
        return value

    def filter_stacktrace(self, data):
        for frame in data.get('frames', []):
            if 'vars' not in frame:
                continue
            frame['vars'] = varmap(self.sanitize, frame['vars'])

    def filter_http(self, data):
        for n in ('data', 'cookies', 'headers', 'env', 'query_string'):
            if n not in data:
                continue

            # data could be provided as bytes and if it's python3
            if not PY2 and isinstance(data[n], bytes):
                data[n] = data[n].decode('utf-8', 'replace')

            if isinstance(data[n], string_types()) and '=' in data[n]:
                # at this point we've assumed it's a standard HTTP query
                # or cookie
                if n == 'cookies':
                    delimiter = ';'
                else:
                    delimiter = '&'

                data[n] = self._sanitize_keyvals(data[n], delimiter)
            else:
                data[n] = varmap(self.sanitize, data[n])
                if n == 'headers' and 'Cookie' in data[n]:
                    data[n]['Cookie'] = self._sanitize_keyvals(
                        data[n]['Cookie'], ';'
                    )

    def filter_extra(self, data):
        return varmap(self.sanitize, data)

    def filter_level(self, data):
        return re.sub(r'\x1b(\[.*?[@-~]|\].*?(\x07|\x1b\\))', '', data)

    def _sanitize_keyvals(self, keyvals, delimiter):
        sanitized_keyvals = []
        for keyval in keyvals.split(delimiter):
            keyval = keyval.split('=')
            if len(keyval) == 2:
                sanitized_keyvals.append((keyval[0], self.sanitize(*keyval)))
            else:
                sanitized_keyvals.append(keyval)

        return delimiter.join('='.join(keyval) for keyval in sanitized_keyvals)


class SanitizePasswordsProcessor(SanitizeKeysProcessor):
    """ Asterisk out things that look like passwords, credit card numbers,
        and API keys in frames, http, and basic extra data. """

    KEYS = frozenset([
        'password',
        'secret',
        'passwd',
        'authorization',
        'api_key',
        'apikey',
        'sentry_dsn',
        'access_token',
    ])
    VALUES_RE = re.compile(r'^(?:\d[ -]*?){13,16}$')

    @property
    def sanitize_keys(self):
        return self.KEYS

    @property
    def FIELDS(self):
        warnings.warn(
            "`SanitizePasswordsProcessor.Fields` has been deprecated. Use "
            "`SanitizePasswordsProcessor.KEYS` or "
            "`SanitizePasswordsProcessor.sanitize_keys` "
            "instead",
            DeprecationWarning,
        )
        return self.KEYS

    def sanitize(self, item, value):
        value = super(SanitizePasswordsProcessor, self).sanitize(item, value)
        if isinstance(value, string_types()) and self.VALUES_RE.match(value):
            return self.MASK
        return value
