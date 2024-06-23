
class AccessError(Exception):
    """
    Base class for exceptions where user is attempting to access infomation
    that they are not authorized to view based on their access level.
    """
class LoginError(AccessError):
    """
    User is attempting to access information that requires user to be logged in.
    """
class ReportError(AccessError):
    """
    Exception when user hasn't submitted a report and context requires that
    a report be completed.
    """

class DatabaseError(Exception): ...
class RequestError(DatabaseError): ...
class WriteError(DatabaseError): ...
class ReadError(DatabaseError): ...
class NoDataError(DatabaseError): ...
class DuplicateUserError(DatabaseError): ...
# This one should throw an error to db

class StateError(Exception): ...

class TokenError(Exception): ...
class ExpiredError(TokenError): ...
