#
# Logs requests to statsd
#
#from urlparse import urlparse
#from eventlet.green import httplib
# 
# Configuration example:
# [filter:keystone_probe]
# paste.filter_factory = keystone_probe.middleware:filter_factory
# host = localhost
# port = 8125
# prefix = dev.syseng.keystone.
# suffix = 
#
#
# Include in pipeline after json_body and xml_body, public API only


from keystone.common import wsgi
from keystone.openstack.common import log as logging
from statsd import Statsd
from webob import Request, Response


class KeystoneProbe(wsgi.Middleware):
    def __init__(self, app, conf):
        self.app = app
        self.config = conf
        self.log = logging.getLogger(__name__)
        self.statsd = Statsd(conf)

    def __call__(self, environ, start_response):
        return self.process_request(environ, start_response)

    def str2bool(self, str):
        if not str:
            return False
        if str in ['false', 'False', 'no', '0']:
            return False
        return True

    def get_username(self, environ):
        '''Extracts auth details from requests and returns a tuple (username, password) if found,
        otherwise returns None'''
        try:
            auth = environ['openstack.params']['auth']['passwordCredentials']
            username = auth['username']
        except KeyError:
            self.log.debug('No authentication context in request')
            return None
        return username

    def statsd_event(self, environ):
        username = self.get_username(environ)
        status_int = environ['statsd.status']
        if username:
            # Authentication request
            username = username.replace('.', '_')
            self.statsd.increment('auth.{0}.{1}'.format(username, status_int))

        path = environ['PATH_INFO']
        method = environ['REQUEST_METHOD']
        # Comment this out for now, generates a lot of excess metrics
        #self.statsd.increment('req.{0}.{1}.{2}'.format(path, method, status_int))

    def process_request(self, environ, start_response):
        def _start_response(status, headers, exc_info=None):
            """start_response wrapper to grab headers and status code"""
            # Convert all headers to lower case
            new_h = [(k.lower(), v) for k,v in headers]
            environ['statsd.headers'] = new_h
            environ['statsd.status'] = int(status.split(' ', 1)[0])
            start_response(status, headers, exc_info)

        # Register a post-hook to be called after the request completes
        if not 'eventlet.posthooks' in environ:
            environ['eventlet.posthooks'] = []
        req = Request(environ)
        environ['eventlet.posthooks'].append((self.statsd_event, (), {}))
        return self.app(environ, _start_response)


def filter_factory(global_conf, **local_conf):
    """Returns a WSGI filter app for use with paste.deploy."""
    conf = global_conf.copy()
    conf.update(local_conf)

    def probe_filter(app):
        return KeystoneProbe(app, conf)
    return probe_filter
