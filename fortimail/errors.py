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
    
    Arguments:
        FortiMailError {Exception} -- The root exception
    '''
    pass
