import logging
from uuid import UUID

import cloudinary
from graphene_file_upload.scalars import Upload

from kaffepause.core.config import settings
from kaffepause.location.exceptions import LocationDoesNotExist
from kaffepause.location.models import Location
from kaffepause.users.models import User

logger = logging.getLogger(__name__)


def change_profile_picture(*, uploaded_by: User, profile_picture: Upload):
    # TODO: save the image url on the user
    return cloudinary.uploader.upload(
        profile_picture,
        folder=settings.PROFILE_PIC_UPLOAD_FOLDER,
        public_id=UUID(uploaded_by.uuid).hex,
        resource_type="image",
        width=100,
        height=100,
        crop="pad",
    )


def update_preferred_location(*, user: User, location_uuid: UUID) -> User:
    location = Location.nodes.get_or_none(uuid=location_uuid)

    if location:
        user.preferred_location.replace(location)
        return user

    logger.info(
        f"Failed to update users preferred location. Location does not exist (uuid:{user.uuid}, location_uuid: {location_uuid})"
    )
    raise LocationDoesNotExist
