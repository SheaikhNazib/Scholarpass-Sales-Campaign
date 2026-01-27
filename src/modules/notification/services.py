from typing import List
from src.modules.notification.adapters import NotificationRepository
from src.modules.notification.models import Notification
from src.modules.notification.schemas import NotificationResponse, NotificationCreate

class NotificationService:
    def __init__(self, repo: NotificationRepository):
        self.repo = repo

    def create_notification(self, req: NotificationCreate) -> NotificationResponse:
        notif = Notification(
            title=req.title,
            message=req.message,
            notification_type=req.notification_type,
            priority=req.priority,
            action_url=req.action_url,
            action_label=req.action_label,
            user_id=req.user_id
        )
        created = self.repo.create(notif)
        return NotificationResponse.from_orm(created)

    def get_user_notifications(self, user_id: int, unread_only: bool = False) -> List[NotificationResponse]:
        notifs = self.repo.get_user_notifications(user_id, unread_only)
        return [NotificationResponse.from_orm(n) for n in notifs]

    def mark_as_read(self, notif_id: int) -> bool:
        return self.repo.mark_as_read(notif_id)

    def delete_notification(self, notif_id: int) -> bool:
        return self.repo.delete(notif_id)
