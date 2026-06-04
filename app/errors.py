import logging
import traceback
import uuid
from typing import Callable, List

from fastapi import Request, Response, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from pydantic_core import ErrorDetails

from app.exceptions import AlphabetBulkException, AlphabetException

logger = logging.getLogger("uvicorn")

CUSTOM_MESSAGES = {
    "string_too_long": "String should have at most {max_length} characters",
    "string_too_short": "String should have at least {min_length} characters",
    "too_short": "List has {actual_length} elements but should have at least {min_length} elements.",
}


def pydantic_error_msg(errors: List[dict]):
    new_errors: List[ErrorDetails] = []
    for error in errors:
        custom_message = CUSTOM_MESSAGES.get(error['type'])
        if custom_message:
            ctx = error.get("ctx")
            error["msg"] = custom_message.format(**ctx) if ctx else custom_message
        new_errors.append(error)
    return new_errors


class RouteErrorHandler(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except Exception as exc:
                if isinstance(exc, AlphabetBulkException):
                    errors = []
                    for e in exc.errors:
                        error_content = {"message": e.message, "location": e.location}
                        if hasattr(e, "path"):
                            error_content["path"] = e.path
                        errors.append(error_content)
                    return JSONResponse(
                        status_code=exc.status_code,
                        content={"errors": errors},
                    )
                elif isinstance(exc, AlphabetException):
                    return JSONResponse(
                        status_code=exc.status_code,
                        content={
                            "errors": [{
                                "message": exc.message,
                                "location": exc.location,
                            }]
                        }
                    )
                elif isinstance(exc, RequestValidationError):
                    errors = pydantic_error_msg(exc.errors())
                    content = {
                        "errors": [
                            {
                                "message": error["msg"],
                                "location": error["loc"][1],
                                "path": error["loc"][1:],
                            } for error in errors
                        ]
                    }
                    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content=content)
                elif isinstance(exc, HTTPException):
                    # Handle FastAPI HTTPException (e.g. 401)
                    return JSONResponse(
                        status_code=exc.status_code,
                        content={
                            "errors": [{
                                "message": exc.detail,
                                "location": None,
                            }]
                        }
                    )
                else:
                    error_id = str(uuid.uuid4())
                    print("ERROR OCCURED", exc)
                    request_body = await request.body()
                    request_body_str = request_body.decode("utf-8")
                    logger.error(
                        f"\nERROR-ID: {error_id}" +
                        f"\nURL: {request.url}" +
                        f"\nBODY: {request_body_str}" +
                        f"\nDETAIL: {traceback.format_exc()}"
                    )
                    return JSONResponse(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content={
                            "error_id": error_id,
                            "detail": traceback.format_exc(),
                        }
                    )

        return custom_route_handler
