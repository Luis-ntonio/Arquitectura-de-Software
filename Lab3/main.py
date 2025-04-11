# main.py

# Importamos lo necesario de database y models
from database import (
    users_db,
    cases_db,
    documents_db,
    attachments_db
)
from models import (
    Case,
    Document,
    Attachment,
    UserRole,
)
from datetime import datetime, timedelta
import random # Para seleccionar una cochera al azar
from fastapi import FastAPI
from functions.auth import router as auth_router
from functions.cases import router as cases_router
from functions.documents import router as documents_router
from functions.users import router as users_router
from functions.status import router as status_router
from functions.attachments import router as attachments_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(cases_router, prefix="/cases", tags=["Cases"])
app.include_router(documents_router, prefix="/documents", tags=["Documents"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(status_router, prefix="/status", tags=["Status"])
app.include_router(attachments_router, prefix="/attachments", tags=["Attachments"])

# Por ahora, usaremos la lógica directamente o funciones de database.py


    

# --- Punto de entrada principal del script ---
if __name__ == "__main__":
    pass