from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.student import StudentManagement
from schemas.student import StudentBaseCreate, StudentBaseUpdat, StudentResponse


def get_all_students(db: Session):
    students = db.query(StudentManagement).all()
    return [StudentResponse.model_validate(s) for s in students], None


def get_student_by_id(db: Session, student_id: int):
    student = db.query(StudentManagement).filter(
        StudentManagement.id == student_id).first()
    if not student:
        return None, "Student Not Found"
    return StudentResponse.model_validate(student), None


def create_student(db: Session, student_in: StudentBaseCreate):
    new_student = StudentManagement(**student_in.model_dump())
    db.add(new_student)
    try:
        db.commit()
        db.refresh(new_student)
        return StudentResponse.model_validate(new_student), None
    except IntegrityError:
        db.rollback()
        return None, "Email already registered"
    except Exception as e:
        db.rollback()
        return None, str(e)


def update_student(db: Session, student_id: int, student_in: StudentBaseUpdat):
    student = db.query(StudentManagement).filter(
        StudentManagement.id == student_id).first()
    if not student:
        return None, "Student Not Found"

    try:
        update_data = student_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(student, key, value)
        db.commit()
        db.refresh(student)
        return StudentResponse.model_validate(student), None
    except IntegrityError:
        db.rollback()
        return None, "Email already exists in another student"
    except Exception as e:
        db.rollback()
        return None, str(e)


def delete_student(db: Session, student_id: int):
    student = db.query(StudentManagement).filter(
        StudentManagement.id == student_id).first()
    if not student:
        return None, "Student Not Found"

    try:
        db.delete(student)
        db.commit()
        return {"message": "Xóa sinh viên thành công"}, None
    except Exception as e:
        db.rollback()
        return None, str(e)
