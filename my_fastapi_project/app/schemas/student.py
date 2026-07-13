from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Any
from datetime import datetime, timezone


class StudentBaseModel(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255,
                           description="Họ tên sinh viên không được để trống!")
    email: EmailStr = Field(
        ..., description="Email sinh viên phải đúng định dạng và không được để trống!")
    major: str = Field(..., min_length=1, max_length=100,
                       description="Ngành học sinh viên không được để trống!")
    gpa: float = Field(..., ge=0.0, le=4.0,
                       description="GPA phải nằm trong khoảng từ 0.0 đến 4.0")


class StudentBaseCreate(StudentBaseModel):
    pass


class StudentBaseUpdat(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    major: Optional[str] = Field(None, min_length=1, max_length=255)
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0)


class BaseResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any] = None
    error: Optional[Any] = None
    path: str
    timestampt: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True
