from .credentials import map_user_credentials
from .user import map_user


def map_all() -> None:
    map_user()
    map_user_credentials()
