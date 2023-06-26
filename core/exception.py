from fastapi import status
from fastapi.responses import JSONResponse


class InvalidUrlInputError(Exception):
    def __init__(self, name: str):
        self.name = name


def exception_404_handler(request: Exception, exc: InvalidUrlInputError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                        content={"message": f"{exc.name} cannot be found."})


