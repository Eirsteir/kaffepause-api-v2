from kaffepause.common.exceptions import DefaultError


class GroupDoesNotExist(DefaultError):
    default_message = "Denne gruppen eksisterer ikke"


class EmptyGroupError(DefaultError):
    default_message = "Gruppen må ha medlemmer."


class CannotLeaveGroupWhenSingleMember(DefaultError):
    default_message = (
        "Du kan ikke forlate gruppen når du er eneste medlem. Du kan kun slette den."
    )
