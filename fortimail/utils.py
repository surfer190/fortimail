from fortimail import exceptions

def raise_for_error(status_code, message=None, errors=None):
    '''
    Helper method to raise exceptions based on the status code of a response 
    received back from Fortimail.

    Arguments:
        status_code {int} -- Status code received in a response from Fortimail
    
    Keyword Arguments:
        message {str} -- Optional message to include in a resulting exception (default: {None})
        errors {list | str} -- Optional errors to include in a resulting exception (default: {None})
    
    Raises:
        exceptions.Forbidden
        exceptions.UnexpectedError
        exceptions.NotFound
    '''
    if status_code == 403:
        raise exceptions.Forbidden(message, errors=errors)
    elif status_code == 404:
        raise exceptions.NotFound(message, errors=errors)
    else:
        raise exceptions.UnexpectedError(message)
