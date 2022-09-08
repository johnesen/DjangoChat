from .exceptions import IncorrectPasswordException


def validate_user_password(password: str, conf_password: str) -> str:
    if password != conf_password:
        raise IncorrectPasswordException('Passwords must match')
    return password
