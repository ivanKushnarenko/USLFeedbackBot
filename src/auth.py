import typing

import db
from user import User


def authorize(user: User):
    db.add_user(user)


def get_authorized_user(user_id: int) -> typing.Optional[User]:
    return db.get_user(user_id)
