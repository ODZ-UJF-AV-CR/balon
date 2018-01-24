#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Tests for my utility functions for dealing with URL query strings.
"""

import string

from hypothesis import given
from hypothesis.strategies import text
import pytest

from myurlparse import get_query_field, set_query_field


@pytest.mark.parametrize(
    'url,field,expected', [
        ('http://example.net', 'foo', []),
        ('http://example.net?foo=bar', 'foo', ['bar']),
        ('http://example.net?foo=bar&foo=baz', 'foo', ['bar', 'baz'])
    ]
)
def test_simple_examples_of_query_get(url, field, expected):
    """
    Test some simple examples with get_query_field().
    """
    assert get_query_field(url, field) == expected


@pytest.mark.parametrize(
    'url,field,value,expected', [
        ('http://example.net', 'hello', 'world', 'http://example.net?hello=world'),
        ('http://example.net?hello=world', 'hello', 'alex', 'http://example.net?hello=world&hello=alex')
    ]
)
def test_simple_examples_of_query_set(url, field, value, expected):
    """
    Test some simple examples with set_query_field() and replace=False.
    """
    assert set_query_field(url, field, value, replace=False) == expected


def test_replacing_url_component():
    """
    Test changing an query string with an existing field with replace=True.
    """
    url      = 'http://example.net?hello=world'
    expected = 'http://example.net?hello=alex'
    assert set_query_field(url, 'hello', 'alex', replace=True) == expected


@given(text(min_size=1))
def test_a_url_with_no_query_string_always_has_empty_values(field):
    """
    If a URL doesn't have a query string, then retrieving field values
    always yields an empty list.
    """
    url = 'http://example.net'
    assert get_query_field(url, field) == []


@given(
    text(min_size=1, alphabet=string.ascii_letters),
    text(min_size=1, alphabet=string.ascii_letters)
)
def test_adding_a_field_is_included_in_the_string(field, value):
    """
    If we add a (field, value) pair to a URL, then they are both present
    in the final URL.
    """
    url = set_query_field('http://example.net', field, value)
    assert field in url
    assert value in url
