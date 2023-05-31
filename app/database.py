from contextlib import asynccontextmanager

from fastapi import FastAPI
from neomodel import config, db

from app.core.config import settings

config.DATABASE_URL = settings.NEO4J_CONNECTION_URL


@asynccontextmanager
async def lifespan(application: FastAPI):
    await initialize_neomodel()
    yield


async def initialize_neomodel():
    # Initialize the Neo4j connection
    config.AUTO_INSTALL_LABELS = True
    config.AUTO_INSTALL_PROPERTIES = True
    config.FORCE_REFRESH_ENTITIES = True
    config.AUTO_INSTALL_RELATIONSHIPS = True
    config.AUTO_CREATE_RELATIONSHIP_TYPE = True
    config.AUTO_CREATE_SCHEMA = True
    config.AUTO_INDEX_SCHEMAS = True
    config.USE_ARRAY_FIELD = True
    config.AUTO_SAVE_ENABLED = True

    await db.set_connection(config.DATABASE_URL)
    await db.set_connection(config.DATABASE_URL + '/' + settings.NEO4J_DATABASE_NAME)

    # Verify the connection
    db.cypher_query("MATCH (n) RETURN n LIMIT 1")
