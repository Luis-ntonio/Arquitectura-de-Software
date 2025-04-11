from fastapi import APIRouter, HTTPException, status
from typing import List
from models import Client
from database import get_all_clients, get_client, create_client, update_client, delete_client, DatabaseError

router = APIRouter()


@router.get("/", response_model=List[Client])
async def read_clients():
    return await get_all_clients()


@router.get("/{client_id}", response_model=Client)
async def read_client(client_id: str):
    try:
        client = await get_client(client_id)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
        return client
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", response_model=Client, status_code=status.HTTP_201_CREATED)
async def create_new_client(client: Client):
    try:
        return await create_client(client.name, client.email, client.phone, client.address)
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{client_id}", response_model=Client)
async def update_existing_client(client_id: str, client: Client):
    try:
        updated_client = await update_client(client_id, client.name, client.email, client.phone, client.address)
        if not updated_client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
        return updated_client
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_client(client_id: str):
    try:
        success = await delete_client(client_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))