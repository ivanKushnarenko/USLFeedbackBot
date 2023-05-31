import typing

from user import UserInfo


_users: dict[int, UserInfo] = {}


def authorize(user_id: int, user: UserInfo):
    _users.update({user_id: user})


def is_authorized(user_id: int) -> bool:
    return user_id in _users


def user_info(user_id: int) -> typing.Optional[UserInfo]:
    if user_id in _users:
        return _users[user_id]
    return None
