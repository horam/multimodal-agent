import logging
import time
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("multimodal_agent.server")


def register_middlewares(app: FastAPI):
    # Middleware: request logging + basic error handling
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        request_id = str(uuid.uuid4())
        start = time.time()
        logger.info(
            "[%s] %s %s",
            request_id,
            request.method,
            request.url.path,
        )
        try:
            response = await call_next(request)
        except HTTPException as exc:
            # Let FastAPI handle HTTPException, but log it
            logger.warning(
                "[%s] HTTPException %s: %s",
                request_id,
                exc.status_code,
                exc.detail,
            )
            raise

        except Exception:
            logger.exception(
                "[%s] Unhandled server error",
                request_id,
            )

            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal server error",
                    "request_id": request_id,
                },
            )

        duration = (time.time() - start) * 1000.0
        logger.info(
            "[%s] %s (%.1f ms)",
            request_id,
            response.status_code,
            duration,
        )
        response.headers["X-Request-ID"] = request_id
        return response
