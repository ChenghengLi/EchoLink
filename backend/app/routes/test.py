from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.post("/test")
async def test():
    return "Hello World!"