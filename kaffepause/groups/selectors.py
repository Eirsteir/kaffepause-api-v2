import logging
from typing import List
from uuid import UUID

from kaffepause.authentication.exceptions import PermissionDenied
from kaffepause.groups.exceptions import GroupDoesNotExist
from kaffepause.groups.models import Group
from kaffepause.users.models import User

logger = logging.getLogger(__name__)


def get_groups_for(user: User) -> List[Group]:
    return user.groups.all()


def get_group(*, actor: User, uuid: UUID) -> Group:
    group = __get_group_or_raise(uuid)

    if not actor.is_member_of(group):
        raise PermissionDenied

    return group


def __get_group_or_raise(uuid):
    try:
        return Group.nodes.get(uuid=uuid)
    except Group.DoesNotExist as e:
        logger.debug(f"Could not find group with uuid: {uuid}", exc_info=e)
        raise GroupDoesNotExist
