import requests
import responses
import pytest

from fortimail.client import FortiMailClient
from fortimail.exceptions import Forbidden, IllegalArgumentError, NotFound

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
        {
            'mkey': 'example.com',
            'maindomain': 'chappy.net',
            'is_association': True
        },
        {
            'mkey': 'caprico.com',
            'maindomain': 'chappy.net',
            'is_association': True
        },
        {
            'mkey': 'zypo.co.uk',
            'maindomain': 'atn.org',
            'is_association': False
        },
        {
            'mkey': 'abc.example.net',
            'maindomain': 'atn.org',
            'is_association': False
        }
    ]
}

DOMAIN_SUCCESS_RESPONSE = {
    'objectID': 'DomainSetting:{D:example.com}',
    'reqAction': 1,
    'nodePermission': 3,
    'mdomain': 'example.com',
    'mxflag': 4,
    'ip': '',
    'port': 25,
    'usessl': False,
    'is_subdomain': False,
    'maindomain': 'example.com',
    'fallbackhost': '',
    'fallbackport': 25,
    'fallbackusessl': False,
    'relay_ip_group': '',
    'remove_outgoing_header': False,
    'alternative_domain_name': '',
    'recipient_verification': 0,
    'alt_smtp_ena': False,
    'alt_smtp_host': '',
    'alt_smtp_port': 25,
    'alt_smtp_ssl': False,
    'recipient_verification_smtp_cmd': 0,
    'recipient_verification_smtp_accept_reply_string_pattern': '',
    'recipient_verification_profile': '',
    'recipient_verification_background': 0,
    'recipient_verification_background_profile': '',
    'tp': '',
    'hide': False,
    'original': False,
    'ldap_routing_state': True,
    'ldap_routing_profile': 'CORPORATE_LDAP',
    'ldap_generic_routing_profile': 'CORPORATE_LDAP',
    'rcptvrfy_try_mhost': False,
    'ldap_asav_state': False,
    'ldap_asav_profile': '',
    'global_bayesian': False,
    'sender_addr_rate_control_state': False,
    'sender_addr_rate_control_max_messages': 50,
    'sender_addr_rate_control_max_messages_state': False,
    'sender_addr_rate_ctrl_max_recipients_state': False,
    'sender_addr_rate_ctrl_max_recipients': 100,
    'sender_addr_rate_control_max_megabytes': 100,
    'sender_addr_rate_control_max_megabytes_state': False,
    'sender_addr_rate_ctrl_max_spam': 10,
    'sender_addr_rate_ctrl_max_spam_state': False,
    'sender_addr_rate_notification_state': False,
    'sender_addr_rate_notification_profile': '',
    'sender_addr_rate_ctrl_action': 125,
    'sender_addr_rate_ctrl_exempt': [],
    'bypass_bounce_verification': False,
    'domain_interval': True,
    'days': 60,
    'hours': 251100,
    'domain_report': True,
    'report_template_name': 'default',
    'domain_recipient': True,
    'other_recipient': False,
    'other_address': '',
    'ldap_group_recipient': False,
    'ldap_profile_groupowner': '',
    'group_recipient_only': False,
    'group_exclude_individual': False,
    'default_language': '',
    'default_theme': -1,
    'ip_pool': '',
    'ip_pool_direction': 1,
    'system_domain': 1,
    'other_greeting': '',
    'ldap_user_profile': '',
    'max_message_size': 204800,
    'addressbook_add_option': 2,
    'ldap_service_status': True,
    'is_service_domain': False,
    'max_mailbox': 10,
    'max_user_quota': 1000,
    'mail_access': 7,
    'webmail_service_type': 0,
    'migration_status': False,
    'relay_auth_status': False,
    'relay_auth_username': 'test',
    'relay_auth_password': '******',
    'relay_auth_type': 0,
    'disclaimer_status': 1,
    'disclaimer_incoming_header_status': False,
    'disclaimer_incoming_header_insertion_name': '',
    'disclaimer_incoming_header_insertion_value': '',
    'disclaimer_incoming_body_status': False,
    'disclaimer_incoming_body_location': 0,
    'disclaimer_incoming_body_content': '',
    'disclaimer_incoming_body_content_html': '',
    'disclaimer_outgoing_header_status': False,
    'disclaimer_outgoing_header_insertion_name': '',
    'disclaimer_outgoing_header_insertion_value': '',
    'disclaimer_outgoing_body_status': False,
    'disclaimer_outgoing_body_location': 0,
    'disclaimer_outgoing_body_content': '',
    'disclaimer_outgoing_body_content_html': '',
    'Type': 0,
    'report_to_domain': '*',
    'reporting_address': 'noreply',
    'domain_association_mxlookup': 0
}

DOMAIN_NOT_FOUND_RESPONSE = {
    'errorType': 3,
    'errorMsg': 'Failed to retrieve object :Get object (DomainSetting) '
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

    @responses.activate
    def test_get_domain(self):
        responses.add(
            responses.POST,
            'https://fortimail.example.com/api/v1/AdminLogin/',
            json=LOGIN_SUCCESS_RESPONSE,
            status=200
        )
        responses.add(
            responses.GET,
            'https://fortimail.example.com/api/v1/domain/example.com',
            json=DOMAIN_SUCCESS_RESPONSE,
            status=200
        )

        client = FortiMailClient(
            baseurl=BASEURL, username=USERNAME, password=PASSWORD
        )

        domain = client.get_domain('example.com')

        assert domain == DOMAIN_SUCCESS_RESPONSE

    @responses.activate
    def test_get_domain_not_found(self):
        '''
        Ensure a not found error is raised for 404
        '''
        responses.add(
            responses.POST,
            'https://fortimail.example.com/api/v1/AdminLogin/',
            json=LOGIN_SUCCESS_RESPONSE,
            status=200
        )
        responses.add(
            responses.GET,
            'https://fortimail.example.com/api/v1/domain/test.com',
            json=DOMAIN_NOT_FOUND_RESPONSE,
            status=404
        )

        client = FortiMailClient(
            baseurl=BASEURL, username=USERNAME, password=PASSWORD
        )

        with pytest.raises(NotFound):
            domain = client.get_domain('test.com')
