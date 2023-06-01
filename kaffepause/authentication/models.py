class UnauthenticatedUser:
    is_active: bool = False

    @property
    def is_authenticated(self) -> bool:
        return False

    @property
    def is_anonymous(self) -> bool:
        return True


class BaseUser:
    id: int
    email: str = ""
    is_active: bool = True
    USERNAME_FIELD: str = "email"

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    def get_username(self):
        return getattr(self, self.USERNAME_FIELD)

    @property
    def identity(self) -> str:
        raise NotImplementedError()  # pragma: no cover
