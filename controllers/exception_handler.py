from fastapi import HTTPException


def handle_exception(exception: Exception) -> HTTPException:
    status_code = 500
    detail = exception
    if isinstance(exception, AttributeError):
        status_code = 404
        detail = "Invalid URL or not found"
    return HTTPException(status_code=status_code, detail=detail)

