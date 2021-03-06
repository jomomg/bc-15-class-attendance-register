from sqlalchemy import Column, Text, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    other_name = Column(String)
    class_id = Column(Integer)

    register_entries = relationship("Register", backref="student")


class ClassTable(Base):
    __tablename__ = "class"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start = Column(DateTime)
    end = Column(DateTime)


class Register(Base):
    __tablename__ = "register"
    entry_id = Column(Integer, primary_key=True)
    class_id = Column(Integer)
    student_id = Column(Integer, ForeignKey("student.id"))
    current_date = Column(DateTime)
    checked_in = Column(Boolean, default=False)
    reason = Column(Text)


def create_db():
    engine = create_engine("sqlite:///attendance_register.db")
    Base.metadata.create_all(engine)
