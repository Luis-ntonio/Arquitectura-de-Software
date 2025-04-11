import hashlib
from fastapi import APIRouter, HTTPException, UploadFile
from database import attachments_db, documents_db
from models import Attachment
from datetime import datetime

router = APIRouter()

def hash_file_name(file_name: str) -> str:
    """
    Hash the file name using SHA-256.
    """
    return hashlib.sha256(file_name.encode()).hexdigest()

@router.post("/upload/")
def upload_attachment(document_id: str, file: UploadFile):
    """
    Upload and hash an attachment for a document.
    """
    if document_id not in documents_db:
        raise HTTPException(status_code=404, detail="Document not found")

    hashed_name = hash_file_name(file.filename)
    file_path = f"/uploads/{hashed_name}"
    attachment_id = f"att_{len(attachments_db) + 1}"
    attachment = Attachment(
        id=attachment_id,
        document_id=document_id,
        file_path=file_path,
        uploaded_at=datetime.now(),
    )
    attachments_db[attachment_id] = attachment.dict()
    return attachment