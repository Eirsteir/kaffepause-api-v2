from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

from app.core.config import settings
from app.schema import schema


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.mount("/graphql/", GraphQLApp(schema,
               on_get=make_graphiql_handler()))  # Graphiql IDE

    # app.mount("/", GraphQLApp(schema)) # no IDE

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()
