from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

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


settings = Settings()
