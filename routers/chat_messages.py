from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from routers.models import ChatMessage, ChatMessageResponse
from config.session import get_db
from business_logic.chat_messages_logic import ChatMessageLogic

router = APIRouter(
    prefix="/chat_messages",
    tags=["chat_messages"]
)

@router.post("/", response_model=ChatMessageResponse)
async def create_chat_message(message: ChatMessage, db: Session = Depends(get_db)):
    try:
        service_logic = ChatMessageLogic(db=db)
        
        service_response = service_logic.save_message(
            user_id=message.user_id,
            role=message.role,
            content=message.content
        )
        return service_response
    
    except Exception as e:
        print("ERROR:", repr(e))
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", response_model=list[ChatMessageResponse])
async def get_chat_messages(db: Session = Depends(get_db)):
    service_logic = ChatMessageLogic(db=db)

    service_response = service_logic.get_messages()
    return service_response
    

