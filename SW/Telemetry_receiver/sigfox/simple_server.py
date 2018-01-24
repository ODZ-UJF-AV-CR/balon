from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse, json


""""
try:  # Python 3+
    from urllib.parse import (
        parse_qs, parse_qsl, urlencode, urlparse, urlunparse
    )
except ImportError:  # Python 2
    from urllib import urlencode
    from urlparse import parse_qs, parse_qsl, urlparse, urlunparse
"""

def get_query_field(url, field):
    """
    Given a URL, return a list of values for the given ``field`` in the
    URL's query string.
    
    >>> get_query_field('http://example.net', field='foo')
    []
    
    >>> get_query_field('http://example.net?foo=bar', field='foo')
    ['bar']
    
    >>> get_query_field('http://example.net?foo=bar&foo=baz', field='foo')
    ['bar', 'baz']
    """
    try:
        return urlparse.parse_qs(urlparse.urlparse(url).query)[field]
    except KeyError:
        return []


class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        message = '\n'.join([
            'CLIENT VALUES:',
            'client_address=%s (%s)' % (self.client_address,
                self.address_string()),
            'command=%s' % self.command,
            'path=%s' % self.path,
            'real path=%s' % parsed_path.path,
            'query=%s' % parsed_path.query,
            'query_value=%s' % get_query_field(self.path,field='data'),
            'request_version=%s' % self.request_version,
            '',
            'SERVER VALUES:',
            'server_version=%s' % self.server_version,
            'sys_version=%s' % self.sys_version,
            'protocol_version=%s' % self.protocol_version,
            '',
            ])
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message)
        return

    def do_POST(self):
        content_len = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_len)
        self.send_response(200)
        self.end_headers()

        data = json.loads(post_body)

        self.wfile.write(data['foo'])
        return

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('', 8080), GetHandler)
    print 'Starting server at http://localhost:8080'
    server.serve_forever()
