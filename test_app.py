import pytest
import sys
import os

# Add the function folder to the path for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'MyFunction'))

import __init__ as myfunc  # Import the function module

from unittest.mock import MagicMock

class DummyRequest:
    def __init__(self, params=None, json_body=None):
        self.params = params or {}
        self._json_body = json_body

    def get_json(self):
        if self._json_body is None:
            raise ValueError("No JSON body")
        return self._json_body

def test_returns_hello_with_name_from_query():
    req = DummyRequest(params={'name': 'World'})
    resp = myfunc.main(req)
    assert resp.status_code == 200
    assert resp.get_body().decode() == "Hello, World!"

def test_returns_hello_with_name_from_body():
    req = DummyRequest(params={}, json_body={'name': 'Azure'})
    resp = myfunc.main(req)
    assert resp.status_code == 200
    assert resp.get_body().decode() == "Hello, Azure!"

def test_returns_400_if_no_name():
    req = DummyRequest(params={}, json_body={})
    resp = myfunc.main(req)
    assert resp.status_code == 400
    assert "Please pass a name" in resp.get_body().decode()

def test_returns_400_if_no_json():
    req = DummyRequest(params={})
    # Simulate ValueError on get_json
    req.get_json = MagicMock(side_effect=ValueError)
    resp = myfunc.main(req)
    assert resp.status_code == 400
    assert "Please pass a name" in resp.get_body().decode()
