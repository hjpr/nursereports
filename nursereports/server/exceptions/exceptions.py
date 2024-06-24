class AuthorizationError(Exception):
    """
    Base class for exceptions involving user accounts and access.
    """


class CreateUserError(AuthorizationError):
    """
    Unable to create user entry in database.
    """


class LoginError(AuthorizationError):
    """
    User is attempting to access information that requires user to be logged in.
    """


class LoginAttemptError(AuthorizationError):
    """
    User did not provide proper credentials to login with.
    """


class NoReportError(AuthorizationError):
    """
    User hasn't submitted a report and context requires that a report be completed.
    """


class DatabaseError(Exception): ...


class RequestError(DatabaseError): ...


class WriteError(DatabaseError): ...


class ReadError(DatabaseError):
    """
    Expected to read information from database that returned nothing.
    """


class NoDataError(DatabaseError): ...


class DuplicateUserError(DatabaseError): ...


# This one should throw an error to db


class StateError(Exception): ...


class TokenError(Exception): ...


class ExpiredError(TokenError): ...
