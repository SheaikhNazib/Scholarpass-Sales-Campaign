from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.modules.connect.services import (
    ConnectChannelService, ConnectTemplateService,
    ConnectMessageService, ConnectCallService
)
from src.modules.connect.repositories import (
    ConnectChannelRepository, ConnectTemplateRepository,
    ConnectMessageRepository, ConnectCallRepository
)
from src.modules.connect.schemas import (
    ConnectChannelSchema, ConnectTemplateSchema,
    ConnectMessageSchema, ConnectCallSchema
)

router = APIRouter(prefix="/api/connect", tags=["connect"])

def get_channel_service(db: Session = Depends(get_db)) -> ConnectChannelService:
    return ConnectChannelService(ConnectChannelRepository(db))

def get_template_service(db: Session = Depends(get_db)) -> ConnectTemplateService:
    return ConnectTemplateService(ConnectTemplateRepository(db))

def get_message_service(db: Session = Depends(get_db)) -> ConnectMessageService:
    return ConnectMessageService(ConnectMessageRepository(db))

def get_call_service(db: Session = Depends(get_db)) -> ConnectCallService:
    return ConnectCallService(ConnectCallRepository(db))

@router.post("/channels", response_model=ConnectChannelSchema, status_code=status.HTTP_201_CREATED)
def create_channel(schema: ConnectChannelSchema, service: ConnectChannelService = Depends(get_channel_service)):
    return service.create_channel(schema)

@router.get("/channels/{channel_id}", response_model=ConnectChannelSchema)
def get_channel(channel_id: int, service: ConnectChannelService = Depends(get_channel_service)):
    channel = service.get_channel(channel_id)
    if not channel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
    return channel

@router.get("/channels", response_model=list[ConnectChannelSchema])
def list_channels(active_only: bool = True, service: ConnectChannelService = Depends(get_channel_service)):
    return service.list_channels(active_only)

@router.put("/channels/{channel_id}", response_model=ConnectChannelSchema)
def update_channel(channel_id: int, schema: ConnectChannelSchema, service: ConnectChannelService = Depends(get_channel_service)):
    updated = service.update_channel(channel_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
    return updated

@router.delete("/channels/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_channel(channel_id: int, service: ConnectChannelService = Depends(get_channel_service)):
    if not service.delete_channel(channel_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")

@router.post("/templates", response_model=ConnectTemplateSchema, status_code=status.HTTP_201_CREATED)
def create_template(schema: ConnectTemplateSchema, service: ConnectTemplateService = Depends(get_template_service)):
    return service.create_template(schema)

@router.get("/templates/{template_id}", response_model=ConnectTemplateSchema)
def get_template(template_id: int, service: ConnectTemplateService = Depends(get_template_service)):
    template = service.get_template(template_id)
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")
    return template

@router.get("/templates/type/{template_type}", response_model=list[ConnectTemplateSchema])
def list_templates_by_type(template_type: str, published_only: bool = True, service: ConnectTemplateService = Depends(get_template_service)):
    return service.list_by_type(template_type, published_only)

@router.get("/templates/category/{category}", response_model=list[ConnectTemplateSchema])
def list_templates_by_category(category: str, service: ConnectTemplateService = Depends(get_template_service)):
    return service.list_by_category(category)

@router.put("/templates/{template_id}", response_model=ConnectTemplateSchema)
def update_template(template_id: int, schema: ConnectTemplateSchema, service: ConnectTemplateService = Depends(get_template_service)):
    updated = service.update_template(template_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")
    return updated

@router.delete("/templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(template_id: int, service: ConnectTemplateService = Depends(get_template_service)):
    if not service.delete_template(template_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")

@router.get("/templates", response_model=list[ConnectTemplateSchema])
def list_all_templates(limit: int = 100, published_only: bool = False, service: ConnectTemplateService = Depends(get_template_service)):
    return service.list_all_templates(limit, published_only)

@router.post("/messages", response_model=ConnectMessageSchema, status_code=status.HTTP_201_CREATED)
def create_message(schema: ConnectMessageSchema, service: ConnectMessageService = Depends(get_message_service)):
    return service.create_message(schema)

@router.get("/messages", response_model=list[ConnectMessageSchema])
def list_messages(limit: int = 100, skip: int = 0, service: ConnectMessageService = Depends(get_message_service)):
    return service.list_all_messages(limit, skip)

@router.get("/messages/{message_id}", response_model=ConnectMessageSchema)
def get_message(message_id: int, service: ConnectMessageService = Depends(get_message_service)):
    message = service.get_message(message_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return message

@router.get("/messages/user/{user_id}", response_model=list[ConnectMessageSchema])
def list_user_messages(user_id: int, limit: int = 20, service: ConnectMessageService = Depends(get_message_service)):
    return service.list_user_messages(user_id, limit)

@router.get("/messages/status/{status}", response_model=list[ConnectMessageSchema])
def list_messages_by_status(status: str, limit: int = 20, service: ConnectMessageService = Depends(get_message_service)):
    return service.list_by_status(status, limit)

@router.get("/messages/thread/{thread_id}", response_model=list[ConnectMessageSchema])
def get_message_thread(thread_id: str, service: ConnectMessageService = Depends(get_message_service)):
    return service.get_thread(thread_id)

@router.put("/messages/{message_id}", response_model=ConnectMessageSchema)
def update_message(message_id: int, schema: ConnectMessageSchema, service: ConnectMessageService = Depends(get_message_service)):
    updated = service.update_message(message_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return updated

@router.post("/messages/{message_id}/send", response_model=ConnectMessageSchema)
def send_message(message_id: int, service: ConnectMessageService = Depends(get_message_service)):
    sent = service.send_message(message_id)
    if not sent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return sent

@router.post("/messages/{message_id}/track-open", response_model=ConnectMessageSchema)
def track_message_open(message_id: int, service: ConnectMessageService = Depends(get_message_service)):
    tracked = service.track_open(message_id)
    if not tracked:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return tracked

@router.post("/messages/{message_id}/track-click", response_model=ConnectMessageSchema)
def track_message_click(message_id: int, service: ConnectMessageService = Depends(get_message_service)):
    tracked = service.track_click(message_id)
    if not tracked:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return tracked

@router.post("/messages/{message_id}/archive", response_model=ConnectMessageSchema)
def archive_message(message_id: int, service: ConnectMessageService = Depends(get_message_service)):
    archived = service.archive_message(message_id)
    if not archived:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return archived

@router.post("/calls", response_model=ConnectCallSchema, status_code=status.HTTP_201_CREATED)
def create_call(schema: ConnectCallSchema, service: ConnectCallService = Depends(get_call_service)):
    return service.create_call(schema)

@router.get("/calls/{call_id}", response_model=ConnectCallSchema)
def get_call(call_id: int, service: ConnectCallService = Depends(get_call_service)):
    call = service.get_call(call_id)
    if not call:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")
    return call

@router.get("/calls/sid/{call_sid}", response_model=ConnectCallSchema)
def get_call_by_sid(call_sid: str, service: ConnectCallService = Depends(get_call_service)):
    call = service.get_by_sid(call_sid)
    if not call:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")
    return call

@router.get("/calls/user/{user_id}", response_model=list[ConnectCallSchema])
def list_user_calls(user_id: int, limit: int = 20, service: ConnectCallService = Depends(get_call_service)):
    return service.list_user_calls(user_id, limit)

@router.get("/calls/status/{status}", response_model=list[ConnectCallSchema])
def list_calls_by_status(status: str, limit: int = 20, service: ConnectCallService = Depends(get_call_service)):
    return service.list_by_status(status, limit)

@router.put("/calls/{call_id}", response_model=ConnectCallSchema)
def update_call(call_id: int, schema: ConnectCallSchema, service: ConnectCallService = Depends(get_call_service)):
    updated = service.update_call(call_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")
    return updated

@router.get("/calls/pending-followup", response_model=list[ConnectCallSchema])
def get_pending_followups(service: ConnectCallService = Depends(get_call_service)):
    return service.get_pending_followups()
