from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from services.student import get_all_students, get_student_by_id, create_student, update_student, delete_student
from database import get_db
from schemas.student import BaseResponse, StudentBaseCreate, StudentBaseUpdat
from typing import Annotated
router = APIRouter(prefix="/student", tags=["API Student"])

db_dependentcy = Annotated[Session, Depends(get_db)]


def send_response(status_code: int, message: str, path: str, data=None, error=None):
    resp_obj = BaseResponse(statusCode=status_code,
                            message=message, path=path, data=data, error=error)
    return JSONResponse(status_code=status_code, content=jsonable_encoder(resp_obj))


@router.get("")
def read_all_students(req: Request, db: Session = Depends(get_db)):
    data, _ = get_all_students(db)
    return send_response(status.HTTP_200_OK, "Lấy danh sách thành công", str(req.url.path), data=data)


@router.get("/{student_id}")
def read_student_detail(student_id: int, req: Request, db: Session = Depends(get_db)):
    data, err = get_student_by_id(db, student_id)
    if err:
        return send_response(status.HTTP_404_NOT_FOUND, "Không tìm thấy sinh viên", str(req.url.path), error=err)
    return send_response(status.HTTP_200_OK, "Lấy chi tiết thành công", str(req.url.path), data=data)


@router.post("")
def add_new_student(student_in: StudentBaseCreate, req: Request, db: Session = Depends(get_db)):
    data, err = create_student(db, student_in)
    if err:
        return send_response(status.HTTP_400_BAD_REQUEST, "Thêm mới thất bại", str(req.url.path), error=err)
    return send_response(status.HTTP_201_CREATED, "Thêm mới thành công", str(req.url.path), data=data)


@router.put("/{student_id}")
def modify_student(student_id: int, student_in: StudentBaseUpdat, req: Request, db: Session = Depends(get_db)):
    data, err = update_student(db, student_id, student_in)
    if err:
        status_code = status.HTTP_404_NOT_FOUND if err == "Student Not Found" else status.HTTP_400_BAD_REQUEST
        return send_response(status_code, "Cập nhật thất bại", str(req.url.path), error=err)
    return send_response(status.HTTP_200_OK, "Cập nhật thành công", str(req.url.path), data=data)


@router.delete("/{student_id}")
def remove_student(student_id: int, req: Request, db: Session = Depends(get_db)):
    data, err = delete_student(db, student_id)
    if err:
        return send_response(status.HTTP_404_NOT_FOUND, "Xóa thất bại", str(req.url.path), error=err)
    return send_response(status.HTTP_200_OK, "Xóa thành công", str(req.url.path), data=data)
