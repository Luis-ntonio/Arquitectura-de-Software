# main.py

# Importamos lo necesario de database y models
from database import (
    users_db,
    cases_db,
    documents_db,
    attachments_db,
    init_sample_data,
    create_user,
    create_case,
    create_document,
    create_attachment
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
import asyncio

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(cases_router, prefix="/cases", tags=["Cases"])
app.include_router(documents_router, prefix="/documents", tags=["Documents"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(status_router, prefix="/status", tags=["Status"])
app.include_router(attachments_router, prefix="/attachments", tags=["Attachments"])

@app.on_event("startup")
async def startup_event():
    # Initialize sample data
    await init_sample_data()

    # Execute happy paths
    await execute_happy_paths()

async def execute_happy_paths():
    print("Executing happy paths...")

    # Step 1: Create a client and an owner
    client = await create_user(
        username="happy_client",
        password="clientpassword",
        role="client",
        email="happy_client@example.com"
    )
    owner = await create_user(
        username="happy_owner",
        password="ownerpassword",
        role="owner",
        email="happy_owner@example.com"
    )
    print(f"Created client: {client}")
    print(f"Created owner: {owner}")

    # Step 2: Client creates a new case with the owner
    case = await create_case(
        attorney_id=owner["id"],
        client_id=client["id"],
        status="open",
        additional_info="Happy path case for testing."
    )
    print(f"Created case: {case}")

    # Step 3: Client uploads a document for the case
    document = await create_document(
        case_id=case["id"],
        file_path="/uploads/happy_case_document.pdf"
    )
    print(f"Uploaded document: {document}")

    # Step 4: Client uploads an attachment for the document
    attachment = await create_attachment(
        document_id=document["id"],
        file_path="/uploads/happy_case_attachment.pdf"
    )
    print(f"Uploaded attachment: {attachment}")

    # Verify the data in the in-memory databases
    print("\n=== In-Memory Databases ===")
    print("Users DB:", users_db)
    print("Cases DB:", cases_db)
    print("Documents DB:", documents_db)
    print("Attachments DB:", attachments_db)

# --- Punto de entrada principal del script ---
if __name__ == "__main__":
    init_sample_data()