import logging.config

from fastapi import FastAPI

from routers import product
from settings import environment
logging.config.dictConfig(environment.settings.LOGGING_CONFIG)

app = FastAPI(title=environment.settings.PROJECT_NAME)

app.include_router(product.router, tags=["Products"], prefix="/api/products")

