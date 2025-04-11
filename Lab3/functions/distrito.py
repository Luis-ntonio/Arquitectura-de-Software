from fastapi import APIRouter, HTTPException, status, Query, Body
from typing import Dict, Any, List, Optional
from database import distrito_db, Distrito
from models import Distrito

router = APIRouter()

router.get("/distritos")
def get_distritos() -> List[Dict[str, Distrito]]:
    return list(distrito_db.values())