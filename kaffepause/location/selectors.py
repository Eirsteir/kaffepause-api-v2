import logging
from typing import Iterable
from uuid import UUID

from kaffepause.location.exceptions import LocationDoesNotExist
from kaffepause.location.models import Location
from kaffepause.users.models import User

logger = logging.getLogger(__name__)


def get_location_or_none(*, location_uuid: UUID):
    return Location.nodes.get_or_none(uuid=location_uuid)


def get_location(*, location_uuid: UUID) -> Location:
    try:
        return Location.nodes.get(uuid=location_uuid)
    except Location.DoesNotExist as e:
        logger.debug(f"Could not find location with uuid: {location_uuid}", exc_info=e)
        raise LocationDoesNotExist


def get_campus_locations(*, actor: User, query: str = None) -> Iterable[Location]:
    locations = Location.nodes.filter(item_type="campus")
    custom_locations = actor.custom_locations

    if query:
        locations.filter(title__icontains=query)
        custom_locations = actor.custom_locations.filter(title__icontains=query)

    return locations.all() + custom_locations.all()
