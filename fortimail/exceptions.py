'''
Errors for the Fortimail client

Having a root exception lets consumers of your API catch exceptions you raise on purpose. 
'''

class FortiMailError(Exception):
    '''
    Base-class for all exceptions raised by this module.
    '''
    def __init__(self, message=None, errors=None):
        if errors:
            message = ', '.join(errors)

        self.errors = errors

        super().__init__(message)

class IllegalArgumentError(FortiMailError):
    '''
    Error raised when a function gets an illegal argument
    '''
    pass

class ClientInitialisationError(FortiMailError):
    '''
    Error raised when the client is not initialised correctly
    '''
    pass

class Forbidden(FortiMailError):
    '''
    Error raised when the client is forbidden
    '''
    pass

class UnexpectedError(FortiMailError):
    pass