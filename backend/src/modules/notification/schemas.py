from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationCreate(BaseModel):
    title: str
    message: Optional[str] = None
    notification_type: Optional[str] = None
    priority: str = "normal"
    action_url: Optional[str] = None
    action_label: Optional[str] = None
    user_id: int

class NotificationResponse(BaseModel):
    id: int
    title: str
    message: Optional[str]
    notification_type: Optional[str]
    priority: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
