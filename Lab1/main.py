from fastapi import FastAPI
from Lab1.api.endpoints import router
from Lab1.database.connection import get_connection
from Lab1.database.models import create_sales_table

app = FastAPI()

@app.on_event("startup")
def startup_event():
    conn = get_connection()
    create_sales_table(conn)
    conn.close()

app.include_router(router)