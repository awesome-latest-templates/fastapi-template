from enum import Enum


class ResponseCode(Enum):
    def __init__(self, code, description=''):
        self.code = code
        self.description = description

    # global exception code
    SUCCESS = (0, "Request fulfilled, document follows")
    BAD_REQUEST = (400, "Bad request syntax or unsupported method")
    UNAUTHORIZED = (401, "No permission")
    FORBIDDEN = (403, "Request forbidden")
    NOT_FOUND = (404, "Data not found")
    DATA_DUPLICATED = (409, "Request data duplicated")
    DATA_UNPROCESSABLED = (422, "The server cannot process your request")
    UNHANDLED_ERROR = (110, "Unhandled system error")
    SYSTEM_ERROR = (500, "System error")

    # auth token
    TOKEN_EXPIRED = (1111, "token expired")
    TOKEN_VALIDATE_FAILED = (1112, "token validate failed")
    TOKNEN_PERMISSION = (1113, "Forbidden request")

    # user part error code
    USER_PASSWORD_EMPTY = (2000, "username or password is empty")
    USER_NOT_FOUND = (2001, "user not found")
    USER_PASSWORD_INVALID = (2002, "password incorrect")
    USER_DISABLED = (2003, "user disabled")
    USER_ALREADY_EXIST = (2004, "user already exists")
    USER_ROLE_INVALID = (2005, "user role name is invalid")

    # file part error code
    FILE_SIZE_EXCEEDED = (3000, "file size exceeded maximum allowed")

    # role part error code
    ROLE_NOT_FOUND = (4000, "role not found")
