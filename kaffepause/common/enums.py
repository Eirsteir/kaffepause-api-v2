from enum import Enum
from uuid import UUID

from kaffepause.core.config import settings

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
        return self.value + str(uuid)
