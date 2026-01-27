from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.modules.notification.adapters import NotificationRepository
from src.modules.notification.services import NotificationService
from src.modules.notification.schemas import NotificationCreate, NotificationResponse

router = APIRouter(prefix="/api/v1/notifications", tags=["notifications"])

def get_notification_service(db: Session = Depends(get_db)) -> NotificationService:
    return NotificationService(NotificationRepository(db))

@router.post("", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
def create_notification(req: NotificationCreate, service: NotificationService = Depends(get_notification_service)):
    return service.create_notification(req)

@router.get("/user/{user_id}", response_model=list[NotificationResponse])
def get_user_notifications(user_id: int, unread_only: bool = False, service: NotificationService = Depends(get_notification_service)):
    return service.get_user_notifications(user_id, unread_only)

@router.patch("/{notif_id}/read")
def mark_as_read(notif_id: int, service: NotificationService = Depends(get_notification_service)):
    if not service.mark_as_read(notif_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return {"message": "Marked as read"}

@router.delete("/{notif_id}")
def delete_notification(notif_id: int, service: NotificationService = Depends(get_notification_service)):
    if not service.delete_notification(notif_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return {"message": "Deleted"}
