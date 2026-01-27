from abc import ABC, abstractmethod
from typing import Optional, List
from src.modules.notification.models import Notification

class INotificationRepository(ABC):
    @abstractmethod
    def create(self, notification: Notification) -> Notification:
        pass

    @abstractmethod
    def get_by_id(self, notif_id: int) -> Optional[Notification]:
        pass

    @abstractmethod
    def get_user_notifications(self, user_id: int, unread_only: bool = False) -> List[Notification]:
        pass

    @abstractmethod
    def mark_as_read(self, notif_id: int) -> bool:
        pass

    @abstractmethod
    def delete(self, notif_id: int) -> bool:
        pass
