import uuid
from typing import Callable

from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
from starlette_context import request_cycle_context
from ..utils.jwt import decode_token


class RequestContextMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = uuid.uuid4().hex

        request_context_data = {
            "request_id": request_id,
        }

        authorization = request.headers.get("Authorization")

        if authorization and authorization.startswith("Bearer "):
            token = authorization[7:]

            try:
                payload = decode_token(token)
                request_context_data["user_id"] = payload.get("sub")
            except (JWTError, ExpiredSignatureError, JWTClaimsError):
                pass

        with request_cycle_context(request_context_data):
            return await call_next(request)
