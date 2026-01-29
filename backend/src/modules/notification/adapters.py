from typing import Optional, List
from sqlalchemy.orm import Session
from src.modules.notification.models import Notification
from src.modules.notification.repositories import INotificationRepository

class NotificationRepository(INotificationRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, notification: Notification) -> Notification:
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def get_by_id(self, notif_id: int) -> Optional[Notification]:
        return self.db.query(Notification).filter(Notification.id == notif_id).first()

    def get_user_notifications(self, user_id: int, unread_only: bool = False) -> List[Notification]:
        query = self.db.query(Notification).filter(Notification.user_id == user_id)
        if unread_only:
            query = query.filter(Notification.is_read == False)
        return query.order_by(Notification.created_at.desc()).all()

    def mark_as_read(self, notif_id: int) -> bool:
        notif = self.get_by_id(notif_id)
        if notif:
            notif.is_read = True
            self.db.commit()
            return True
        return False

    def delete(self, notif_id: int) -> bool:
        notif = self.get_by_id(notif_id)
        if notif:
            self.db.delete(notif)
            self.db.commit()
            return True
        return False
