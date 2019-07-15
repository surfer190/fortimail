import requests
import pytest

from fortimail.client import FortiMailClient
from fortimail.errors import IllegalArgumentError

class TestFortimailClient(object):

    def test_client_create(self):
        '''
        Ensure the client instance is crated
        '''
        client = FortiMailClient()

    def test_session_accepted_keyword_arg(self):
        '''
        Ensure the session can be set for the client
        '''
        session = requests.Session()
        client = FortiMailClient(session=session)
    
    def test_session_is_requests_session(self):
        '''
        Ensure the session given is a requests Session
        '''
        session = {'hello': 'world'}
        with pytest.raises(IllegalArgumentError):
            client = FortiMailClient(session=session)
