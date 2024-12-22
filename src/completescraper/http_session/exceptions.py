class LoginError(Exception):
    pass


class InvalidPasswordError(LoginError):
    pass
