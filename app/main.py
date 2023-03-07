from fastapi import Request, FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
import logging
import uvicorn

from database import DBConnector
from functions.startupVariables import StartupVariables

from routes import *

system_variables = StartupVariables()
debug = os.getenv("DEBUG")

# Initialize logging
logging.basicConfig(
    level=(
        logging.DEBUG if debug else logging.INFO
    ),
    format='\033[31m%(levelname)s\033[0m \033[90min\033[0m \033[33m%(filename)s\033[0m \033[90mon\033[0m %(asctime)s\033[90m:\033[0m %(message)s',
    datefmt='\033[32m%m/%d/%Y\033[0m \033[90mat\033[0m \033[32m%H:%M:%S\033[0m'
)
logging.getLogger("fastapi").setLevel(logging.ERROR)
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("motor").setLevel(logging.ERROR)
logging.getLogger(__name__)
if debug:
    logging.info("static.env - 'DEBUG' key found. Running in debug mode, do not use in production.")


def create_app():
    new_app = FastAPI(
        title="Central API",
        description="IPL Central API Service",
        docs_url="/internaldocs",
        redoc_url="/docs"
    )
    # Set up DB & API connections
    new_app.db = DBConnector(system_variables.database_uri, system_variables.db_name)

    # Startup and Shutdown Events
    @new_app.on_event("startup")
    async def startup():
        await new_app.db.connect_db()

    @new_app.on_event("shutdown")
    async def shutdown():
        await new_app.db.close_mongo_connection()
    # Add cors
    new_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add session middleware
    new_app.add_middleware(SessionMiddleware, secret_key=system_variables.session_secret, max_age=10800)

    # Routes


    # Define OpenAPI info
    def custom_openapi():
        if new_app.openapi_schema:
            return new_app.openapi_schema
        openapi_schema = get_openapi(
            title="ReTails API",
            description="🤷‍♀️",
            version="1.0.0",
            routes=new_app.routes,
            tags=[
            ]
        )
        new_app.openapi_schema = openapi_schema
        return new_app.openapi_schema

    new_app.openapi = custom_openapi

    # Include Routes
    return new_app


app = create_app()
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=2000)
