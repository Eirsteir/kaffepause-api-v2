from enum import Enum
from uuid import UUID

from kaffepause.core.config import settings


class BaseStatusEnum(Enum):
    """
    Mirrors :class:`StatusModel` in which subclasses have to define
    member variables in the form of a tuple (verb, slug).
    The name member variable is inferred from the name of the attribute.
    """

    def __call__(self, *args, **kwargs):
        """Avoid having to call `.slug` in every query where slug is often the most relevant lookup field."""
        return self.slug

    @property
    def verb(self):
        return self.value[0]

    @property
    def slug(self):
        return self.value[1]


# TODO: put in settings
ACCOUNT = "kaffepause.accounts.models.Account"
SESSION = "kaffepause.accounts.models.Session"
USER = "kaffepause.users.models.User"
BREAK = "kaffepause.breaks.models.Break"
BREAK_INVITATION = "kaffepause.breaks.models.BreakInvitation"
CHANGE_REQUEST = "kaffepause.breaks.models.ChangeRequest"
STATUS_UPDATE = "kaffepause.statusupdates.models.StatusUpdate"
LOCATION = "kaffepause.location.models.Location"
NOTIFICATION = "kaffepause.notifications.models.Notification"
GROUP = "kaffepause.groups.models.Group"


class Endpoints(Enum):
    GROUPS = f"{settings.WEBSITE_URL}/groups/"
    USERS = f"{settings.WEBSITE_URL}/users/"
    BREAKS = f"{settings.WEBSITE_URL}/breaks/"

    def single(self, uuid: UUID):
        return self.value + uuid
