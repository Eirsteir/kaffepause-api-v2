import os

environment = os.getenv("APP_ENV", "PRODUCTION")

if environment == "DEVELOPMENT":
    import kaffepause.core.settings.local

    settings = kaffepause.core.settings.local.settings
else:
    import kaffepause.core.settings.production

    settings = kaffepause.core.settings.production.settings
