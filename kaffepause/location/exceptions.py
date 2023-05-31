from kaffepause.common.exceptions import DefaultError


class LocationDoesNotExist(DefaultError):
    default_message = "Dette stedet finnes ikke"
