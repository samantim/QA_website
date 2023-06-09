from db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

#it is inherited from Base which is an as_declarative -> makes it possible to create tables automatically
class Answer(Base):
    __tablename__ = "answers" #name in db
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    date_posted = Column(DateTime, nullable=False)
    is_correct = Column(Boolean, default=False)
    attachment_path = Column(String)
    user_id = Column(Integer, ForeignKey("users.id")) 
    question_id = Column(Integer, ForeignKey("questions.id"))
    replier = relationship("User", back_populates="answers")
    question = relationship("Question", back_populates="replies")
