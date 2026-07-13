from sqlalchemy import Integer, String, Column, Float
from database import Base


class StudentManagement(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    full_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    major = Column(String(255), nullable=True)
    gpa = Column(Float, nullable=True)
