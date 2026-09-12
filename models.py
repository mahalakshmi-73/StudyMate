from sqlalchemy import Column, Integer, String, Float 
from database import Base

class StudentDB(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String)
    study_hours = Column(Float)
    mark = Column(Float)
    level = Column(String)
    suggestion = Column(String)