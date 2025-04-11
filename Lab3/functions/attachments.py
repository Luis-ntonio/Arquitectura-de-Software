from fastapi import APIRouter, HTTPException, status, UploadFile, File
from typing import List
from models import Attachment
from database import get_all_attachments, get_attachment, create_attachment, update_attachment, delete_attachment, DatabaseError

router = APIRouter()


@router.get("/cases/{case_id}/attachments", response_model=List[Attachment])
async def read_case_attachments(case_id: str):
    try:
        all_attachments = await get_all_attachments()
        return [a for a in all_attachments if a.case_id == case_id]
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{attachment_id}", response_model=Attachment)
async def read_attachment(attachment_id: str):
    try:
        attachment = await get_attachment(attachment_id)
        if not attachment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")
        return attachment
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/cases/{case_id}/attachments", response_model=Attachment, status_code=status.HTTP_201_CREATED)
async def upload_attachment(case_id: str, file: UploadFile = File(...)):
    # In a real application, implement file saving and URL generation
    try:
        attachment = await create_attachment(
            name=file.filename,
            type=file.content_type,
            size=file.size,
            url=f"/files/{file.filename}",  # Placeholder URL
            case_id=case_id
        )
        return attachment
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{attachment_id}", response_model=Attachment)
async def update_existing_attachment(attachment_id: str, attachment: Attachment):
    try:
        updated_attachment = await update_attachment(
            attachment_id,
            name=attachment.name,
            type=attachment.type,
            size=attachment.size,
            url=attachment.url,
            case_id=attachment.case_id
        )
        if not updated_attachment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")
        return updated_attachment
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_attachment(attachment_id: str):
    try:
        success = await delete_attachment(attachment_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))