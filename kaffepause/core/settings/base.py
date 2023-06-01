from datetime import timedelta
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class AppBaseSettings(BaseSettings):
    PROJECT_NAME: str = "kaffepause"
    DEBUG: bool = False
    TIME_ZONE: str = "Europe/Oslo"
    WEBSITE_URL: str = "https://kaffepause.eiriksteira.com"

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # NEO4J
    # ------------------------------------------------------------------------------
    NEO4J_USER: str
    NEO4J_PASSWORD: str
    NEO4J_HOST: str
    NEO4J_PORT: str
    NEO4J_CONNECTION_URL: Optional[str] = None

    @validator("NEO4J_CONNECTION_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return (
            f"neo4j+s://{values.get('NEO4J_USER')}:{values.get('NEO4J_PASSWORD')}"
            f"@{values.get('NEO4J_HOST')}:{values.get('NEO4J_PORT')}"
        )

    # JWT
    # ------------------------------------------------------------------------------
    JWT_AUTH_HEADER_NAME: str = "Authorization"
    JWT_AUTH_HEADER_PREFIX: str = "JWT"
    JWT_COOKIE_NAME: str = "JWT"
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_DELTA: timedelta = timedelta(days=30)

    class Config:
        case_sensitive = True
