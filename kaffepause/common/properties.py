import uuid

from neomodel import UniqueIdProperty


class UUIDProperty(UniqueIdProperty):
    """
    A unique identifier, a randomly generated uid (uuid4) with a unique index.
    Uses the UUID object instead of hex value for a simpler overall implementation.
    """

    def __init__(self, **kwargs):
        for item in ["required", "unique_index", "index", "default"]:
            if item in kwargs:
                raise ValueError(
                    "{0} argument ignored by {1}".format(item, self.__class__.__name__)
                )

        kwargs["unique_index"] = True
        kwargs["default"] = lambda: uuid.uuid4()
        super(UniqueIdProperty, self).__init__(**kwargs)
