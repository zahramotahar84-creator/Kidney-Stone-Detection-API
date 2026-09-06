# -*- coding: utf-8 -*-
#cd kidey_Project
# uvicorn untitled19:app --reload
"""
Created on Sun Aug  2 10:13:04 2026

@author: user
"""
#cd C:\Users\user\.spyder-py3
#"C:\ProgramData\anaconda3\python.exe" -m uvicorn untitled19:app --reload
from fastapi import FastAPI, HTTPException, status, File, Depends, UploadFile
from fastapi.responses import FileResponse # For serving the images
from sqlalchemy.orm import Session
from typing import List, Optional

# Import from your existing files
from database import SessionLocal, engine, Base, get_db, UserDB
from file_utils import save_upload_file, UPLOAD_DIR
from pydantic import BaseModel, Field, EmailStr
from untitled20 import EmailAlreadyExistsException, UserNotFoundException
from madel_handler import get_prediction
# --- Pydantic Models for Validation ---
class UserOutput(BaseModel):
    id: int
    name: str
    age: int
    email: str
    image_path: Optional[str] = None

    class Config:
        from_attributes = True

class UserRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    age: int = Field(..., ge=10, le=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)

class UserResponse(BaseModel):
    message: str
    user: Optional[UserOutput] = None

# --- App Initialization ---
app = FastAPI(title="Anti-Bug User API")

# --- API Endpoints ---

@app.post("/user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(request: UserRequest, db: Session = Depends(get_db)):
    """Create a new user in Database"""
    existing_user = db.query(UserDB).filter(UserDB.email == request.email).first()
    if existing_user:
        raise EmailAlreadyExistsException()
    
    new_user = UserDB(
        name=request.name,
        age=request.age,
        email=request.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user": new_user}

@app.get("/user/{user_id}", response_model=UserOutput)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID from Database"""
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise UserNotFoundException()
    return user

@app.post("/upload-image/{user_id}")
async def upload_image(user_id: int, file: UploadFile = File(...)):
    """
    This function receives the image, saves it, and uses the AI model to diagnose.
    """
    try:
        # Step 1: Save the image using your file_utils function
        file_path = save_upload_file(file) 
        
        if not file_path:
            return {"status": "error", "message": "Could not save the uploaded file."}

        # Step 2: Send the path to the AI model for prediction
        diagnosis, confidence = get_prediction(file_path)
        
        # Step 3: Return the final result to the user
        return {
            "status": "success",
            "user_id": user_id,
            "filename": file.filename,
            "analysis": {
                "diagnosis": diagnosis,
                "confidence": f"{confidence:.2f}%"
            },
            "message": "Image analyzed successfully!"
        }

    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {str(e)}"}


@app.get("/user/image/{user_id}")
async def get_user_image(user_id: int, db: Session = Depends(get_db)):
    """Retrieve and display the image file of the user"""
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user or not user.image_path:
        raise HTTPException(status_code=404, detail="User image not found in database")
    
    return FileResponse(user.image_path)

@app.get("/search", response_model=List[UserOutput])
async def search_users(name: Optional[str] = None, age: Optional[int] = None, db: Session = Depends(get_db)):
    """Search users by name and/or age in Database"""
    query = db.query(UserDB)
    if name:
        query = query.filter(UserDB.name.contains(name))
    if age:
        query = query.filter(UserDB.age == age)
    return query.all()

@app.delete("/user/{user_id}", status_code=204)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user from Database"""
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise UserNotFoundException()
    
    db.delete(user)
    db.commit()
    return None