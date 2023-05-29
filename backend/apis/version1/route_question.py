from fastapi import APIRouter, Depends, HTTPException, status
from schemas.questions import Question_Create, Question_Show
from db.session import get_db
from sqlalchemy.orm import Session
from db.models.users import User
from apis.version1.route_login import get_current_active_user
from db.repository.questions import create_question, read_all_questions, read_question_by_id, delete_question_by_id


question_router = APIRouter()

@question_router.post("", response_model=Question_Show)
def add_question(question : Question_Create, db : Session = Depends(get_db), current_active_user : User = Depends(get_current_active_user)):
    question = create_question(question, db, current_active_user)
    if not question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create a question!")
    return question

@question_router.get("/get/all", response_model=list[Question_Show])
def show_all_questions(db : Session = Depends(get_db), current_active_user : User = Depends(get_current_active_user)):
    if not current_active_user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to retrieve all questions!")
    questions = read_all_questions(db)
    return questions

@question_router.get("/{id}", response_model=Question_Show)
def show_question(question_id : int, db : Session = Depends(get_db)):
    question = read_question_by_id(question_id, db)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Question id {question_id} not found!")
    return question

@question_router.delete("/delete/{id}")
def delete_question(question_id : int, db : Session = Depends(get_db), current_active_user : User = Depends(get_current_active_user)):
    if not current_active_user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to delete questions!")
    result = delete_question_by_id(question_id, db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No question to delete!")
    return {"msg" : f"Question id {question_id} seccessfully deleted!"}