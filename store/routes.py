from .images import ChatType, Route
from .operating import get_session


def routes_by_vkpeer(vk_peer: int) -> list[Route]:
    return get_session().query(Route).filter(Route.vk_peer == vk_peer).all()


def route_by_tgchatid(tg_chat_id: int) -> Route:
    return get_session().query(Route).filter(Route.tg_chat_id == tg_chat_id).first()


def routes_by_tguserid(tg_userid: int):
    return get_session().query(Route).filter(Route.tg_userid == tg_userid).all()


def routes_by_vkuserid(vk_userid: int):
    return get_session().query(Route).filter(Route.vk_userid == vk_userid).all()


def _chat_type(vk_peer: int) -> ChatType:
    return get_session().query(Route).filter(Route.vk_peer == vk_peer).first().chat_type


def new_route(route: Route):
    get_session().merge(route)
