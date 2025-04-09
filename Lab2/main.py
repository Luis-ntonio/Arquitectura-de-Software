from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from functions import auth, cocheras, reservas, review
from functions.other import router as other_router
import uvicorn
from database import init_sample_data

async def lifespan_context_manager(app: FastAPI):
    """
    Lifespan context manager to handle startup and shutdown events.
    Initializes sample data during the startup phase.
    """
    # Perform startup tasks - call directly without await since it's not async
    init_sample_data()
    yield
    # Perform shutdown tasks (if any)
    # Add any necessary cleanup code here

# Initialize the FastAPI application
app = FastAPI(
    title="Kuadra - Parking Spot Rental",
    description="API for renting parking spots using FastAPI",
    version="0.2.0",
    lifespan=lifespan_context_manager,  # Set the lifespan context manager
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with prefixes and tags
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(cocheras.router, prefix="/api/cocheras", tags=["Parking Spots"])
app.include_router(reservas.router, prefix="/api/reservas", tags=["Reservations"])
app.include_router(review.router, prefix="/api/reviews", tags=["Reviews"])
app.include_router(other_router, prefix="/api/services", tags=["Additional Services"])