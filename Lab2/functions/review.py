from fastapi import APIRouter, HTTPException, Body, status, Query
from typing import Dict, Any, List, Optional
from datetime import datetime

from database import reviews_db, cocheras_db, reservas_db, users_db, generate_id, update_cochera_rating, get_user_by_username
from models import ReviewCreate, ReviewUpdate, ReviewResponse

router = APIRouter()

@router.get("/", response_model=List[ReviewResponse])
def list_reviews(
    cochera_id: Optional[str] = Query(None, description="Filter reviews by parking spot ID")
):
    """
    List reviews with optional filtering by parking spot.
    """
    result = []
    
    for review_id, data in reviews_db.items():
        if cochera_id and data["cochera_id"] != cochera_id:
            continue
        result.append({
            "review_id": review_id,
            **data
        })
    
    return result

@router.get("/user", response_model=List[ReviewResponse])
def list_user_reviews(
    username: str = Body(..., embed=True)  # Pass username directly
):
    """
    Get all reviews created by the specified user.
    """
    current_user = get_user_by_username(username)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")
    
    result = []
    for review_id, data in reviews_db.items():
        if data["user_id"] == current_user["user_id"]:
            result.append({
                "review_id": review_id,
                **data
            })
    
    return result

@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(review_id: str):
    """
    Get details for a specific review.
    """
    if review_id not in reviews_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Review not found"
        )
    
    return {
        "review_id": review_id,
        **reviews_db[review_id]
    }

@router.post("/", response_model=ReviewResponse)
def create_review(
    review: ReviewCreate,
    username: str = Body(..., embed=True)  # Pass username directly
):
    """
    Create a new review for a parking spot.
    Only clients can create reviews.
    """
    current_user = get_user_by_username(username)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")
    
    if current_user["role"] != "client":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only clients can create reviews"
        )
    
    if review.cochera_id not in cocheras_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking spot not found"
        )
    
    for reserva in reservas_db.values():
        if (reserva["user_id"] == current_user["user_id"] and 
            reserva["cochera_id"] == review.cochera_id and
            reserva["status"] == "completed"):
            has_used = True
            break
    if not has_used:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only review parking spots you have used"
        )
    
    # Check if the user has already reviewed this parking spot
    for r in reviews_db.values():
        if r["user_id"] == current_user["user_id"] and r["cochera_id"] == review.cochera_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already reviewed this parking spot"
            )
    
    review_id = generate_id()
    created_at = datetime.now().isoformat()
    
    reviews_db[review_id] = {
        "user_id": current_user["user_id"],
        "cochera_id": review.cochera_id,
        "rating": review.rating,
        "comment": review.comment,
        "created_at": created_at
    }
    
    # Update the parking spot's average rating
    update_cochera_rating(review.cochera_id)
    
    return {
        "review_id": review_id,
        **reviews_db[review_id]
    }

@router.patch("/{review_id}", response_model=ReviewResponse)
def update_review(
    review_id: str,
    update_data: ReviewUpdate,
    username: str = Body(..., embed=True)  # Pass username directly
):
    """
    Update a review.
    Users can only update their own reviews.
    """
    current_user = get_user_by_username(username)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")
    
    if review_id not in reviews_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Review not found"
        )
    
    # Check if the user is the author of the review
    if reviews_db[review_id]["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own reviews"
        )
    
    # Update fields if provided
    if update_data.rating is not None:
        reviews_db[review_id]["rating"] = update_data.rating
    if update_data.comment is not None:
        reviews_db[review_id]["comment"] = update_data.comment
    
    # Update the parking spot's average rating
    update_cochera_rating(reviews_db[review_id]["cochera_id"])
    
    return {
        "review_id": review_id,
        **reviews_db[review_id]
    }

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: str,
    username: str = Body(..., embed=True)  # Pass username directly
):
    """
    Delete a review.
    Users can only delete their own reviews.
    """
    current_user = get_user_by_username(username)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")
    
    if review_id not in reviews_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Review not found"
        )
    
    # Check if the user is the author of the review
    if reviews_db[review_id]["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own reviews"
        )
    
    cochera_id = reviews_db[review_id]["cochera_id"]
    del reviews_db[review_id]
    
    # Update the parking spot's average rating
    update_cochera_rating(cochera_id)
