from typing import List
from uuid import UUID

from kaffepause.authentication.exceptions import PermissionDenied
from kaffepause.groups.exceptions import (
    CannotLeaveGroupWhenSingleMember,
    EmptyGroupError,
)
from kaffepause.groups.models import Group
from kaffepause.groups.selectors import get_group
from kaffepause.notifications.enums import NotificationEntityType
from kaffepause.notifications.services import bulk_notify
from kaffepause.users.models import User
from kaffepause.users.selectors import get_user


def create_group(*, actor: User, name: str, members: List[UUID]) -> Group:
    contains_only_actor = all(m_uuid == actor.uuid for m_uuid in members)
    if not members or contains_only_actor:
        raise EmptyGroupError

    group = Group(name=name).save()
    group.creator.connect(actor)
    group.members.connect(actor)

    members = actor.friends.filter(uuid__in=members)
    add_members_to_group(actor, group, members)

    return group


def add_members_to_group(actor: User, group: Group, members: [User]):
    for member in members:
        group.members.connect(member)

    bulk_notify(
        notifiers=members,
        actor=actor,
        entity_type=NotificationEntityType.GROUP_MEMBER_ADDED,
        entity_id=group.uuid,
        group_name=group.name,
    )


def remove_group_member(*, actor: User, group_uuid: UUID, member_uuid: UUID) -> Group:
    group = get_group(actor=actor, uuid=group_uuid)
    member_to_remove = get_user(uuid=member_uuid)

    if not actor.is_member_of(group):
        raise PermissionDenied

    actor_leaves_as_last_member = (
        len(group.members.all()) == 1 and str(member_uuid) == actor.uuid
    )
    if actor_leaves_as_last_member:
        raise CannotLeaveGroupWhenSingleMember

    group.members.disconnect(member_to_remove)

    return group


def add_group_members(
    *, actor: User, group_uuid: UUID, user_uuids: List[UUID]
) -> Group:
    group = get_group(actor=actor, uuid=group_uuid)

    if not actor.is_member_of(group):
        raise PermissionDenied

    users = User.nodes.filter(uuid__in=user_uuids)
    add_members_to_group(actor=actor, group=group, members=users)

    return group


def edit_group_name(*, actor: User, group_uuid: UUID, name: str) -> Group:
    group = get_group(actor=actor, uuid=group_uuid)
    old_name = name
    group.name = old_name
    group.save()
    bulk_notify(
        notifiers=group.members.exclude(uuid=actor.uuid),
        actor=actor,
        entity_type=NotificationEntityType.GROUP_NAME_CHANGED,
        entity_id=group.uuid,
        group_name=old_name,
        new_group_name=name,
    )
    return group
