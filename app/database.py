from contextlib import asynccontextmanager

from fastapi import FastAPI
from neomodel import config

from app.core.config import settings


@asynccontextmanager
async def lifespan(application: FastAPI):
    await initialize_neomodel()
    yield


async def initialize_neomodel():
    # Initialize the Neo4j connection
    config.DATABASE_URL = settings.NEO4J_CONNECTION_URL

    config.AUTO_INSTALL_LABELS = True
    config.AUTO_INSTALL_PROPERTIES = True
    config.FORCE_REFRESH_ENTITIES = True
    config.AUTO_INSTALL_RELATIONSHIPS = True
    config.AUTO_CREATE_RELATIONSHIP_TYPE = True
    config.AUTO_CREATE_SCHEMA = True
    config.AUTO_INDEX_SCHEMAS = True
    config.USE_ARRAY_FIELD = True
    config.AUTO_SAVE_ENABLED = True
