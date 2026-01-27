from typing import Optional, List, Protocol
from sqlalchemy.orm import Session
from datetime import datetime
from src.modules.connect.models import ConnectChannel, ConnectTemplate, ConnectMessage, ConnectCall

class IConnectChannelRepository(Protocol):
    def create(self, channel: ConnectChannel) -> ConnectChannel: ...
    def get_by_id(self, channel_id: int) -> Optional[ConnectChannel]: ...
    def get_by_code(self, code: str) -> Optional[ConnectChannel]: ...
    def list_all(self, active_only: bool = True) -> List[ConnectChannel]: ...
    def update(self, channel_id: int, **kwargs) -> Optional[ConnectChannel]: ...
    def delete(self, channel_id: int) -> bool: ...

class IConnectTemplateRepository(Protocol):
    def create(self, template: ConnectTemplate) -> ConnectTemplate: ...
    def get_by_id(self, template_id: int) -> Optional[ConnectTemplate]: ...
    def list_by_type(self, template_type: str, published_only: bool = True) -> List[ConnectTemplate]: ...
    def list_by_category(self, category: str) -> List[ConnectTemplate]: ...
    def update(self, template_id: int, **kwargs) -> Optional[ConnectTemplate]: ...
    def delete(self, template_id: int) -> bool: ...
    def increment_usage(self, template_id: int) -> None: ...

class IConnectMessageRepository(Protocol):
    def create(self, message: ConnectMessage) -> ConnectMessage: ...
    def get_by_id(self, message_id: int) -> Optional[ConnectMessage]: ...
    def list_by_user(self, user_id: int, limit: int = 20) -> List[ConnectMessage]: ...
    def list_by_status(self, status: str, limit: int = 20) -> List[ConnectMessage]: ...
    def list_by_thread(self, thread_id: str) -> List[ConnectMessage]: ...
    def update(self, message_id: int, **kwargs) -> Optional[ConnectMessage]: ...
    def mark_as_sent(self, message_id: int) -> Optional[ConnectMessage]: ...
    def mark_as_opened(self, message_id: int) -> Optional[ConnectMessage]: ...
    def mark_as_clicked(self, message_id: int) -> Optional[ConnectMessage]: ...
    def archive(self, message_id: int) -> Optional[ConnectMessage]: ...

class IConnectCallRepository(Protocol):
    def create(self, call: ConnectCall) -> ConnectCall: ...
    def get_by_id(self, call_id: int) -> Optional[ConnectCall]: ...
    def get_by_sid(self, call_sid: str) -> Optional[ConnectCall]: ...
    def list_by_user(self, user_id: int, limit: int = 20) -> List[ConnectCall]: ...
    def list_by_status(self, status: str, limit: int = 20) -> List[ConnectCall]: ...
    def update(self, call_id: int, **kwargs) -> Optional[ConnectCall]: ...
    def list_pending_followup(self) -> List[ConnectCall]: ...

class ConnectChannelRepository(IConnectChannelRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, channel: ConnectChannel) -> ConnectChannel:
        self.db.add(channel)
        self.db.commit()
        self.db.refresh(channel)
        return channel

    def get_by_id(self, channel_id: int) -> Optional[ConnectChannel]:
        return self.db.query(ConnectChannel).filter(ConnectChannel.id == channel_id).first()

    def get_by_code(self, code: str) -> Optional[ConnectChannel]:
        return self.db.query(ConnectChannel).filter(ConnectChannel.code == code).first()

    def list_all(self, active_only: bool = True) -> List[ConnectChannel]:
        query = self.db.query(ConnectChannel)
        if active_only:
            query = query.filter(ConnectChannel.is_active == True)
        return query.order_by(ConnectChannel.display_order).all()

    def update(self, channel_id: int, **kwargs) -> Optional[ConnectChannel]:
        channel = self.get_by_id(channel_id)
        if channel:
            for key, value in kwargs.items():
                setattr(channel, key, value)
            self.db.commit()
            self.db.refresh(channel)
        return channel

    def delete(self, channel_id: int) -> bool:
        channel = self.get_by_id(channel_id)
        if channel:
            self.db.delete(channel)
            self.db.commit()
            return True
        return False

class ConnectTemplateRepository(IConnectTemplateRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, template: ConnectTemplate) -> ConnectTemplate:
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template

    def get_by_id(self, template_id: int) -> Optional[ConnectTemplate]:
        return self.db.query(ConnectTemplate).filter(ConnectTemplate.id == template_id).first()

    def list_by_type(self, template_type: str, published_only: bool = True) -> List[ConnectTemplate]:
        query = self.db.query(ConnectTemplate).filter(ConnectTemplate.template_type == template_type)
        if published_only:
            query = query.filter(ConnectTemplate.published == True)
        return query.all()

    def list_by_category(self, category: str) -> List[ConnectTemplate]:
        return self.db.query(ConnectTemplate).filter(
            ConnectTemplate.category == category,
            ConnectTemplate.published == True
        ).all()

    def update(self, template_id: int, **kwargs) -> Optional[ConnectTemplate]:
        template = self.get_by_id(template_id)
        if template:
            for key, value in kwargs.items():
                setattr(template, key, value)
            self.db.commit()
            self.db.refresh(template)
        return template

    def delete(self, template_id: int) -> bool:
        template = self.get_by_id(template_id)
        if template and not template.is_system_template:
            self.db.delete(template)
            self.db.commit()
            return True
        return False

    def increment_usage(self, template_id: int) -> None:
        template = self.get_by_id(template_id)
        if template:
            template.usage_count += 1
            template.last_used_at = datetime.utcnow()
            self.db.commit()

class ConnectMessageRepository(IConnectMessageRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, message: ConnectMessage) -> ConnectMessage:
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_by_id(self, message_id: int) -> Optional[ConnectMessage]:
        return self.db.query(ConnectMessage).filter(ConnectMessage.id == message_id).first()

    def list_by_user(self, user_id: int, limit: int = 20) -> List[ConnectMessage]:
        return self.db.query(ConnectMessage).filter(
            ConnectMessage.sender_user_id == user_id
        ).order_by(ConnectMessage.created_at.desc()).limit(limit).all()

    def list_by_status(self, status: str, limit: int = 20) -> List[ConnectMessage]:
        return self.db.query(ConnectMessage).filter(
            ConnectMessage.status == status
        ).order_by(ConnectMessage.created_at.desc()).limit(limit).all()

    def list_by_thread(self, thread_id: str) -> List[ConnectMessage]:
        return self.db.query(ConnectMessage).filter(
            ConnectMessage.thread_id == thread_id
        ).order_by(ConnectMessage.created_at.asc()).all()

    def update(self, message_id: int, **kwargs) -> Optional[ConnectMessage]:
        message = self.get_by_id(message_id)
        if message:
            for key, value in kwargs.items():
                setattr(message, key, value)
            self.db.commit()
            self.db.refresh(message)
        return message

    def mark_as_sent(self, message_id: int) -> Optional[ConnectMessage]:
        return self.update(message_id, status='sent', sent_at=datetime.utcnow())

    def mark_as_opened(self, message_id: int) -> Optional[ConnectMessage]:
        return self.update(message_id, is_opened=True, opened_at=datetime.utcnow(), open_count=ConnectMessage.open_count + 1)

    def mark_as_clicked(self, message_id: int) -> Optional[ConnectMessage]:
        return self.update(message_id, is_clicked=True, clicked_at=datetime.utcnow(), click_count=ConnectMessage.click_count + 1)

    def archive(self, message_id: int) -> Optional[ConnectMessage]:
        return self.update(message_id, message_archived=True, archived_at_date=datetime.utcnow())

class ConnectCallRepository(IConnectCallRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, call: ConnectCall) -> ConnectCall:
        self.db.add(call)
        self.db.commit()
        self.db.refresh(call)
        return call

    def get_by_id(self, call_id: int) -> Optional[ConnectCall]:
        return self.db.query(ConnectCall).filter(ConnectCall.id == call_id).first()

    def get_by_sid(self, call_sid: str) -> Optional[ConnectCall]:
        return self.db.query(ConnectCall).filter(ConnectCall.call_sid == call_sid).first()

    def list_by_user(self, user_id: int, limit: int = 20) -> List[ConnectCall]:
        return self.db.query(ConnectCall).filter(
            ConnectCall.user_id == user_id
        ).order_by(ConnectCall.initiated_at.desc()).limit(limit).all()

    def list_by_status(self, status: str, limit: int = 20) -> List[ConnectCall]:
        return self.db.query(ConnectCall).filter(
            ConnectCall.status == status
        ).order_by(ConnectCall.initiated_at.desc()).limit(limit).all()

    def update(self, call_id: int, **kwargs) -> Optional[ConnectCall]:
        call = self.get_by_id(call_id)
        if call:
            for key, value in kwargs.items():
                setattr(call, key, value)
            self.db.commit()
            self.db.refresh(call)
        return call

    def list_pending_followup(self) -> List[ConnectCall]:
        return self.db.query(ConnectCall).filter(
            ConnectCall.follow_up_required == True,
            ConnectCall.follow_up_date <= datetime.utcnow()
        ).all()
