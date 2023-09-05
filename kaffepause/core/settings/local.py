from typing import Any, Dict, Optional

from pydantic import validator

from kaffepause.core.settings.base import AppBaseSettings


class Settings(AppBaseSettings):
    DEBUG: bool = True

    @validator("NEO4J_CONNECTION_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return (
            f"neo4j+s://{values.get('NEO4J_USER')}:{values.get('NEO4J_PASSWORD')}"
            f"@{values.get('NEO4J_HOST')}:{values.get('NEO4J_PORT')}"
        )


settings = Settings()
