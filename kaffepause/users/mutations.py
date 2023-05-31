import logging

import graphene
from graphene_file_upload.scalars import Upload

from kaffepause.common.bases import LoginRequiredMixin, Output
from kaffepause.location.models import Location
from kaffepause.location.types import LocationNode
from kaffepause.users.services import change_profile_picture, update_preferred_location
from kaffepause.users.types import UserNode

logger = logging.getLogger(__name__)


class ChangeProfilePicture(LoginRequiredMixin, Output, graphene.Mutation):
    class Arguments:
        image = Upload(required=True)

    user = graphene.Field(UserNode)
    image = graphene.String()

    @classmethod
    def resolve_mutation(cls, root, info, profile_pic, **kwargs):
        current_user = info.context.user

        result = change_profile_picture(
            uploaded_by=current_user, profile_picture=profile_pic
        )
        return cls(profile_pic=result.get("secure_url"))


class UpdatePreferredLocation(LoginRequiredMixin, Output, graphene.Mutation):
    class Arguments:
        location_uuid = graphene.UUID(required=True)

    user = graphene.Field(UserNode)
    location = graphene.Field(LocationNode)

    @classmethod
    def resolve_mutation(cls, root, info, location_uuid, **kwargs):
        current_user = info.context.user

        try:
            user = update_preferred_location(
                user=current_user, location_uuid=location_uuid
            )
            logger.debug(
                f"Successfully updated users preferred location (uuid:{user.uuid}, location_uuid: {location_uuid})"
            )
        except Location.DoesNotExist as e:
            return cls(success=False, errors=["Dette stedet eksisterer ikke"])

        return cls(success=True, user=user)
