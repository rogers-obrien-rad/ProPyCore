class ProcoreException(Exception):
    """
    The base exception class for Procore.
    Parameters:
        msg (str): Short description of the error.
        response: Error response from the API call.
    """

    def __init__(self, msg, response=None):
        super(ProcoreException, self).__init__(msg)
        self.message = msg
        self.response = response

    def __str__(self):
        return repr(self.message)


class NotFoundClientError(ProcoreException):
    """Client not found OAuth2 authorization, 404 error."""
    pass


class UnauthorizedClientError(ProcoreException):
    """Wrong client secret and/or refresh token, 401 error."""
    pass


class ExpiredTokenError(ProcoreException):
    """Expired (old) access token, 498 error."""
    pass


class InvalidTokenError(ProcoreException):
    """Wrong/non-existing access token, 401 error."""
    pass


class NoPrivilegeError(ProcoreException):
    """The user has insufficient privilege, 403 error."""
    pass


class WrongParamsError(ProcoreException):
    """Some of the parameters (HTTP params or request body) are wrong, 400 error."""
    pass


class NotFoundItemError(ProcoreException):
    """Not found the item from URL, 404 error."""
    pass
    

class InternalServerError(ProcoreException):
    """The rest Procore errors, 500 error."""
    pass

class UnprocessableContentError(ProcoreException):
    """Non-unique field, 422 error."""
    pass

def raise_exception(response):
    """
    Raises an exception based on the provided status code

    Parameters
    ----------
    status_code : int
        valid get/request code
    """
    if response.status_code == 401:
        raise UnauthorizedClientError('401: Wrong client secret or/and refresh token', response.text)
    
    elif response.status_code == 403:
        raise NoPrivilegeError(f"403: Data connection app or permission template does not have access to this endpoint", response.text)

    elif response.status_code == 404:
        raise NotFoundClientError('404: Client ID doesn\'t exist', response.text)

    elif response.status_code == 422:
        raise UnprocessableContentError('422: A field that needs a unique value already exists', response.text)

    elif response.status_code == 500:
        raise InternalServerError('500: Internal server error', response.text)

    else:
        raise ProcoreException('Error: {0}'.format(response.status_code), response.text)