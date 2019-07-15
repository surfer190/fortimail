import requests

from .errors import IllegalArgumentError

class FortiMailClient(object):
    
    def __init__(self, session=None):
        if not session:
            session = requests.Session()
        
        # check if session is an instance of requests session
        if not isinstance(session, requests.Session):
            raise IllegalArgumentError('Session needs to be of type requests.Session')
        self.session = session
