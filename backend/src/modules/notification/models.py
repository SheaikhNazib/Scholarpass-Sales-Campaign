from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from datetime import datetime
from src.infrastructure.database import Base

class Notification(Base):
    __tablename__ = "app_notifications"
    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    message = Column(Text)
    notification_type = Column(String(50))
    priority = Column(String(20), default="normal")
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime)
    action_url = Column(String(1024))
    action_label = Column(String(128))
    user_id = Column(Integer, ForeignKey("app_users.id", ondelete="CASCADE"), nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
