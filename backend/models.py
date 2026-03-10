from sqlalchemy import Column, Integer, String
from database import Base

class NewsCheck(Base):
    __tablename__ = "news_checks"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    result = Column(String)
    score = Column(Integer)


class ImageCheck(Base):
    __tablename__ = "image_checks"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    result = Column(String)
    score = Column(Integer)