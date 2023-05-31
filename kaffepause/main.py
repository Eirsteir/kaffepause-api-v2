from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

from kaffepause.api.schema import schema
from kaffepause.core.config import settings
from kaffepause.database import lifespan


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

    if settings.DEBUG:
        _app.mount("/graphql/", GraphQLApp(schema, on_get=make_graphiql_handler()))
    else:
        app.mount("/", GraphQLApp(schema))

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()
