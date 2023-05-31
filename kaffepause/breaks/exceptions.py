from kaffepause.common.exceptions import DefaultError


class BreakNotFound(DefaultError):
    default_message = "Denne pausen finnes ikke"


class InvitationExpired(DefaultError):
    default_message = "Invitasjonen er utgått."


class AlreadyReplied(DefaultError):
    default_message = "Du har allerede svart på invitasjonen."


class BreakInvitationExpiresBeforeStartTime(DefaultError):
    default_message = "Invitasjonen kan ikke utgå før pausen skal starte"


class InvalidInvitationExpiration(DefaultError):
    default_message = "Utløpstiden for invitasjonen er ugyldig"


class InvalidInvitationRecipients(DefaultError):
    default_message = (
        "Invitasjonen kan ikke ha både individuelle brukere og en gruppe som mottaker."
    )


class InvalidInvitationUpdate(DefaultError):
    default_message = "Kunne ikke oppdatere invitasjonen"


class InvalidBreakStartTime(DefaultError):
    default_message = "Pausen må begynne i fremtiden."


class InvitationNotAddressedAtUser(DefaultError):
    default_message = "Denne invitasjonen er ikke rettet mot denne brukeren."


class MissingOrIdenticalTimeAndLocationInChangeRequestException(DefaultError):
    default_message = "Forslaget må inkludere enten en ny tid eller nytt sted."


class InvalidChangeRequestForExpiredBreak(DefaultError):
    default_message = "Du kan ikke komme med endringsforslag til denne pausen lengre."


class InvalidChangeRequestRequestedTime(DefaultError):
    default_message = "Forslag til ny til må være minst 5 minutter frem i tid."
