import requests

from fortimail.exceptions import IllegalArgumentError
from fortimail.utils import raise_for_error


class FortiMailClient(object):
    def __init__(self, baseurl, username, password, session=None):
        '''Initialise the Fortimail client

        Arguments:
            baseurl {str} -- URL of the fortimail server
            username {str} -- username
            password {str} -- password

        Keyword Arguments:
            session {requests.Session} -- Supply existing session

        Raises:
            IllegalArgumentError: If session is not of requests.Session
        '''
        if not session:
            session = requests.Session()

        # check if session is an instance of requests session
        if not isinstance(session, requests.Session):
            raise IllegalArgumentError(
                'Session needs to be of type requests.Session'
            )
        self.session = session
        self.baseurl = baseurl
        self.username = username
        self.password = password

        # remove slash
        self.api_url = '{}/api/v1'.format(self.baseurl)

        self.session.verify = False

        self.login()

    def login(self):
        '''
        Login to the fortimail server and store the token
        '''
        login_url = '{}/AdminLogin/'.format(self.api_url)
        data = {'name': self.username, 'password': self.password}

        response = self.session.post(
            url=login_url,
            json=data
        )

        if response.status_code != 200:
            if response.headers.get('Content-Type') == 'application/json':
                errors = response.json().get('errors')
                json = response.json()
            raise_for_error(response.status_code, json, errors=errors)
        # should store cookie

    def get_domains(self):
        '''
        Get a list of all domains
        '''
        response = self.session.get('{}/domain/'.format(self.api_url))
        if response.status_code != 200:
            raise_for_error(response.status_code, response.json())
        return response.json()

    def get_domain(self, domain_name):
        '''
        Get a single domain

        Arguments:
            domain_name {str} -- fqn of the domain
        '''
        response = self.session.get('{url}/domain/{domain}'.format(
            url=self.api_url,
            domain=domain_name
        ))
        if response.status_code != 200:
            raise_for_error(response.status_code, response.json())
        return response.json()
