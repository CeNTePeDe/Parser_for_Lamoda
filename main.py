import logging.config

from fastapi import FastAPI

from config.dev import settings, LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI(title=settings.PROJECT_NAME)


#
# @app.post("/")
# async def get_url_for_parsing(url: UrlSchema):
#     pass
