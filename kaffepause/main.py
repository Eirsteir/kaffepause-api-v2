from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from kaffepause.api.graphql_app import graphql_app
from kaffepause.core.config import settings
from kaffepause.core.database import lifespan


def get_application():
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        lifespan=lifespan,
        open_api_url=None,
        debug=settings.DEBUG,
    )

    _app.mount("/graphql", graphql_app)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()
