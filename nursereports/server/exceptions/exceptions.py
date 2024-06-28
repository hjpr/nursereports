from loguru import logger

import traceback


class AuthorizationError(Exception):
    """Base class for exceptions involving user accounts and access."""

    def __init__(self, error_message):
        super().__init__(error_message)
        stack = traceback.extract_stack()
        func = stack[-2]
        logger.critical(f"{func} - {error_message}")


class CreateUserFailed(AuthorizationError):
    """Unable to create user entry in database."""


class LoginError(AuthorizationError):
    """User is attempting to access information that requires user to be logged in."""


class LoginCredentialsInvalid(AuthorizationError):
    """User did not provide proper credentials to login with."""


class NoReportError(AuthorizationError):
    """User hasn't submitted a report and context requires that a report be completed."""


class DatabaseError(Exception):
    def __init__(self, error_message):
        super().__init__(error_message)
        stack = traceback.extract_stack()
        func = stack[-2]
        logger.critical(f"{func} - {error_message}")


class RequestFailed(DatabaseError): ...


class WriteError(DatabaseError): ...


class ReadError(DatabaseError):
    """Expected to read information from database that returned nothing."""


class NoDataError(DatabaseError): ...


class DuplicateUserError(DatabaseError): ...


# This one should throw an error to db


class FormError(Exception):
    def __init__(self, error_message):
        super().__init__(error_message)
        stack = traceback.extract_stack()
        func = stack[-2]
        logger.critical(f"{func} - {error_message}")


class InvalidError(FormError):
    """User is attempting to enter a value that is invalid, or
    a field was left empty."""


class TokenError(Exception):
    def __init__(self, error_message):
        super().__init__(error_message)
        stack = traceback.extract_stack()
        func = stack[-2]
        logger.critical(f"{func} - {error_message}")


class ExpiredError(TokenError): ...
