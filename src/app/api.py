from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .constants.config import Settings
from .routers.user_router import router as user_router
from .routers.auth_router import router as auth_router
from .routers.vendor_router import router as vendor_router
from .routers.job_router import router as job_router
from .routers.review_router import router as review_router
from .routers.item_router import router as item_router
from .routers.assignment_router import router as assignment_router
from .routers.question_router import router as question_router
from .routers.student_answer_router import router as student_answer_router
from fastapi.staticfiles import StaticFiles
from .middleware.request_context import RequestContextMiddleware
from .middleware.request_logging import RequestLoggingMiddleware
from .db.database import PSQLManager
from .models._base_model import _metadata_obj
import os

settings = Settings()
PREFIX = f"/api/{settings.API_VERSION}"
_metadata_obj.create_all(bind=PSQLManager.Instance().get_base_engin(), checkfirst=True)

app = FastAPI(
    openapi_url=f"{PREFIX}/openapi.json",
    docs_url=f"{PREFIX}/docs",
    redoc_url=f"{PREFIX}/redoc",
)
app.mount(
    "/static",
    StaticFiles(
        directory=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        + "/static",
        html=False,
    ),
    name="static",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestContextMiddleware)
app.add_middleware(RequestLoggingMiddleware)

# Include the router
app.include_router(auth_router, tags=["Authenication"], prefix=f"{PREFIX}/auth")
app.include_router(user_router, tags=["User"], prefix=f"{PREFIX}/user")
# app.include_router(vendor_router, tags=["Vendor"], prefix=f"{PREFIX}/vendor")
# app.include_router(job_router, tags=["Job"], prefix=f"{PREFIX}/job")
# app.include_router(review_router, tags=["Review"], prefix=f"{PREFIX}/review")
# app.include_router(item_router, tags=["Item"], prefix=f"{PREFIX}/item")
app.include_router(assignment_router, tags=["Assignment"], prefix=f"{PREFIX}/assignment")
app.include_router(question_router, tags=["Question"], prefix=f"{PREFIX}/question")
app.include_router(student_answer_router, tags=["Auto-grader"], prefix=f"{PREFIX}/auto")




