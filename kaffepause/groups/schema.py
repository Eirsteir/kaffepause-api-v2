import graphene

from kaffepause.authentication.decorators import login_required
from kaffepause.groups.mutations import (
    AddGroupMembers,
    CreateGroup,
    EditGroupName,
    RemoveGroupMember,
)
from kaffepause.groups.selectors import get_group, get_groups_for
from kaffepause.groups.types import GroupNode


class Query(graphene.ObjectType):
    my_groups = graphene.List(GroupNode)
    group = graphene.Field(GroupNode, uuid=graphene.UUID(required=True))

    @login_required
    def resolve_my_groups(self, info, **kwargs):
        current_user = info.context["user"]
        return get_groups_for(user=current_user)

    @login_required
    def resolve_group(self, info, uuid, **kwargs):
        current_user = info.context["user"]
        return get_group(actor=current_user, uuid=uuid)


class Mutation(graphene.ObjectType):
    create_group = CreateGroup.Field()
    remove_group_member = RemoveGroupMember.Field()
    add_group_members = AddGroupMembers.Field()
    edit_group_name = EditGroupName.Field()
