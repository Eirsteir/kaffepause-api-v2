from typing import Optional

import sentry_sdk
from pydantic import HttpUrl, validator

# https://chat.openai.com/c/dcd76169-d3de-4b5c-8e8d-e257595f2546
from kaffepause.core.settings.base import AppBaseSettings


class ProductionSettings(AppBaseSettings):
    # Sentry
    # ------------------------------------------------------------------------------
    SENTRY_DSN: HttpUrl

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if len(v) == 0:
            return None
        return v

    @validator("SENTRY_DSN", pre=True)
    def init_sentry(cls, v: str) -> Optional[str]:
        sentry_sdk.init(
            dsn=v,
            traces_sample_rate=1.0,
        )
        return v


settings = ProductionSettings()
