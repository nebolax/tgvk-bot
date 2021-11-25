from .images import User
from .operating import get_session


def user_by_tgid(tgid: int) -> User:
    return get_session().query(User).filter(User.tg_id == tgid).first()


def user_by_vkid(vkid: int) -> User:
    return get_session().query(User).filter(User.tg_id == vkid).first()


def new_user(user: User) -> None:
    get_session().add(user)


def all_users() -> list[User]:
    return get_session().query(User).all()
