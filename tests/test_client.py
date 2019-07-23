import requests
import responses
import pytest

from fortimail.client import FortiMailClient
from fortimail.exceptions import Forbidden, IllegalArgumentError

USERNAME = 'admin'
PASSWORD = 'my_pass'
BASEURL = 'https://fortimail.example.com'

# status 403
LOGIN_FAILED_RESPONSE = {
    'errorType': 7,
    'errorMsg': 'Failed: Access denied:Add object (AdminLogin) ',
    'reqAction': 2,
    'totalRemoteCount': 0,
    'collection': '[]'
}

# status = 200
LOGIN_SUCCESS_RESPONSE = {
    'objectID': 'AdminLogin:',
    'reqAction': 2,
    'nodePermission': 0,
    'name': 'admin',
    'password': '******',
    'new_password': '******',
    'token': '******',
    'domain': 'system',
    'webmode': 1,
    'locale': 'en',
    'loginstatus': 1,
    'model': 'FE-3LD',
    'serial': 'FE-3LD0001',
    'theme': 0,
    'operation_mode': 2,
    'manager_supported': 0,
    'debug': False,
    'product_name': 'FortiMail',
    'product_version': '6.0.143',
    'post_login_banner': False,
    'disclaimer': '',
    'is_superadmin': False,
    'scramble': True,
    'forced_encryption': 3,
    'migration_enabled': False,
    'dlp_enabled': True,
    'minimum_length': 8,
    'must_contain': 0
}

DOMAINS_SUCCESS_RESPONSE = {
    'objectID': 'DomainInfoCollection:',
    'reqAction': 1,
    'totalRemoteCount': 4,
    'subCount': 4,
    'remoteSorting': True,
    'nextPage': False,
    'nodePermission': 3,
    'collection': [
        {'mkey': 'example.com', 'maindomain': 'chappy.net', 'is_association': True},
        {'mkey': 'caprico.com', 'maindomain': 'chappy.net', 'is_association': True},
        {'mkey': 'zypo.co.uk', 'maindomain': 'atn.org', 'is_association': False},
        {'mkey': 'abc.example.net', 'maindomain': 'atn.org', 'is_association': False}
    ]
}

class TestFortimailClient(object):

    @responses.activate
    def test_client_create(self):
        '''
        Ensure the client instance is created (login is called)
        '''
        responses.add(
            responses.POST,
            'https://fortimail.example.com/api/v1/AdminLogin/',
            json=LOGIN_SUCCESS_RESPONSE,
            status=200
        )
        client = FortiMailClient(
            username=USERNAME,
            password=PASSWORD,
            baseurl=BASEURL
        )

    @responses.activate
    def test_client_login_failed(self):
        '''
        Ensure an exception is raised when the login failed
        '''
        responses.add(
            responses.POST,
            'https://fortimail.example.com/api/v1/AdminLogin/',
            json=LOGIN_FAILED_RESPONSE,
            status=403
        )
        with pytest.raises(Forbidden):
            client = FortiMailClient(
                username=USERNAME,
                password=PASSWORD,
                baseurl=BASEURL
            )

    @responses.activate
    def test_session_accepted_keyword_arg(self):
        '''
        Ensure the session can be set for the client
        '''
        responses.add(
            responses.POST,
            'https://fortimail.example.com/api/v1/AdminLogin/',
            json=LOGIN_SUCCESS_RESPONSE,
            status=200
        )
        session = requests.Session()
        client = FortiMailClient(
            session=session,
            username=USERNAME,
            password=PASSWORD,
            baseurl=BASEURL
        )

    @responses.activate
    def test_session_is_requests_session(self):
        '''
        Ensure the session given is a requests Session
        '''
        session = {'hello': 'world'}
        with pytest.raises(IllegalArgumentError):
            client = FortiMailClient(
                session=session,
                username=USERNAME,
                password=PASSWORD,
                baseurl=BASEURL
            )

    @responses.activate
    def test_no_baseurl_raises_error(self):
        with pytest.raises(TypeError):
            client = FortiMailClient(username=USERNAME, password=PASSWORD)

    @responses.activate
    def test_no_password_raises_error(self):
        with pytest.raises(TypeError):
            client = FortiMailClient(username=USERNAME, baseurl=BASEURL)

    @responses.activate
    def test_no_username_raises_error(self):
        with pytest.raises(TypeError):
            client = FortiMailClient(baseurl=BASEURL, password=PASSWORD)

    @responses.activate
    def test_get_domains(self):
        responses.add(
            responses.POST,
            'https://fortimail.example.com/api/v1/AdminLogin/',
            json=LOGIN_SUCCESS_RESPONSE,
            status=200
        )
        responses.add(
            responses.GET,
            'https://fortimail.example.com/api/v1/domain/',
            json=DOMAINS_SUCCESS_RESPONSE,
            status=200
        )
        
        client = FortiMailClient(
            baseurl=BASEURL, username=USERNAME, password=PASSWORD
        )
        
        domains = client.get_domains()
        
        assert domains == DOMAINS_SUCCESS_RESPONSE
