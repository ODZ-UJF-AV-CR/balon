#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Utility functions for dealing with URL query strings in Python,
i.e., URLs of the form

    http://example.net?field1=value1&field2=value2

This module includes a pair of helper functions: one for getting the values
associated with a particular field; another for setting the query string
values within a URL.
"""

try:  # Python 3+
    from urllib.parse import (
        parse_qs, parse_qsl, urlencode, urlparse, urlunparse
    )
except ImportError:  # Python 2
    from urllib import urlencode
    from urlparse import parse_qs, parse_qsl, urlparse, urlunparse


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
        return parse_qs(urlparse(url).query)[field]
    except KeyError:
        return []


def set_query_field(url, field, value, replace=False):
    """
    Given a URL and a new field/value pair, add the new field/value to
    the URL's query string.  If ``replace`` is True, replace any existing
    instances of this field.  e.g.
    
    >>> set_query_field('http://example.net', field='hello', value='world')
    'http://example.net?hello=world'
    
    >>> set_query_field('http://example.net?hello=world', 'hello', 'alex')
    'http://example.net?hello=world&hello=alex'
    
    >>> set_query_field('http://example.net?hello=world',
                        field='hello', value='alex', replace=True)
    'http://example.net?hello=alex'
    
    >>> set_query_field('http://example.net?hello=world&foo=bar',
                        field='hello', value='alex', replace=True)
    'http://example.net?hello=alex&foo=bar'
    """
    # Parse out the different parts of the URL.
    components = urlparse(url)
    query_pairs = parse_qsl(urlparse(url).query)

    if replace:
        query_pairs = [(f, v) for (f, v) in query_pairs if f != field]
    query_pairs.append((field, value))

    new_query_str = urlencode(query_pairs)

    # Finally, construct the new URL
    new_components = (
        components.scheme,
        components.netloc,
        components.path,
        components.params,
        new_query_str,
        components.fragment
    )
    return urlunparse(new_components)
