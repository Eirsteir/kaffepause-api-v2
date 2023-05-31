import logging
from datetime import datetime, timedelta

from jose import JWTError, jwt

from kaffepause.core.config import settings
from kaffepause.users.models import User

logger = logging.getLogger(__name__)


def get_user_by_natural_key(email):
    logger.debug(f"Auth: getting user by natural key: {email}")

    try:
        return User.nodes.get(email=email)
    except User.DoesNotExist as e:
        logger.error(f"Auth: User not found : {email}", exc_info=e)
        return None


def get_username_from_user(payload):
    return payload.get(User.USERNAME_FIELD)


def get_http_authorization(request):
    auth = request.META.get(settings.JWT_AUTH_HEADER_NAME, "").split()
    prefix = settings.JWT_AUTH_HEADER_PREFIX
    if len(auth) != 2 or auth[0].lower() != prefix.lower():
        return None
    return auth[1]


def get_credentials(request, **kwargs):
    return get_http_authorization(request)


def get_user_by_token(token, context=None):
    payload = get_payload(token, context)
    return get_user_by_payload(payload)


def get_payload(token, context=None):
    try:
        payload = decode_jwt(token, context)
    except JWTError:
        raise JWTError("Error decoding token")
    return payload


def get_user_by_payload(payload):
    email = get_username_from_user(payload)

    if not email:
        raise JWTError("Invalid payload")

    user = get_user_by_natural_key(email)

    if user is not None and not user.is_active:
        raise JWTError("User is disabled")
    return user


def decode_jwt(token: str, context=None):
    return jwt.decode(
        token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )


def encode_jwt(token):
    return jwt.encode(token, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_access_token(user: User, expires_delta: timedelta = None):
    to_encode = jwt_payload(user, expires_delta)
    encoded_jwt = encode_jwt(to_encode)
    return encoded_jwt


def jwt_payload(user: User, expires_delta: timedelta = None):
    username = user.get_username()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + settings.JWT_EXPIRATION_DELTA

    payload = {user.USERNAME_FIELD: username, "exp": expire, "user_id": str(user.id)}

    # if jwt_settings.JWT_ALLOW_REFRESH:
    #     payload['origIat'] = timegm(datetime.utcnow().utctimetuple())

    return payload
