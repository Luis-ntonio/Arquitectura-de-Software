import hashlib
from fastapi import APIRouter, HTTPException, UploadFile
from database import documents_db
from models import Document
from datetime import datetime

router = APIRouter()

def hash_file_name(file_name: str) -> str:
    return hashlib.sha256(file_name.encode()).hexdigest()

@router.post("/upload/")
def upload_document(case_id: str, file: UploadFile):
    hashed_name = hash_file_name(file.filename)
    file_path = f"/uploads/{hashed_name}"
    document_id = f"doc_{len(documents_db) + 1}"
    document = Document(
        id=document_id,
        case_id=case_id,
        file_path=file_path,
        uploaded_at=datetime.now(),
    )
    documents_db[document_id] = document.dict()
    return document