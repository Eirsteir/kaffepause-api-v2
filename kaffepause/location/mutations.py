import logging

import graphene

from kaffepause.common.bases import LoginRequiredMixin, Output
from kaffepause.location.services import add_user_location
from kaffepause.location.types import LocationNode

logger = logging.getLogger(__name__)


class AddUserLocation(LoginRequiredMixin, Output, graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)

    location = graphene.Field(LocationNode)

    @classmethod
    def resolve_mutation(cls, root, info, title):
        user = info.context["user"]
        location = add_user_location(user=user, title=title)
        logger.debug(
            f"Successfully added user location "
            f"(uuid:{location.uuid}, user_uuid:{user.uuid})"
        )
        return cls(success=True, location=location)
