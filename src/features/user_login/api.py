from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(request: LoginRequest):
    # TODO: Implement authentication logic
    if request.username == "admin" and request.password == "password":
        return {"message": "Login successful", "user": {"username": "admin"}}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
