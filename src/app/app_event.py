
from .db.database import PSQLManager

from .api import app


@app.on_event("startup")
def startup_event():
    PSQLManager.Instance()

