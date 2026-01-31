from typing import Optional, List
from src.modules.connect.repositories import (
    ConnectChannelRepository, ConnectTemplateRepository, 
    ConnectMessageRepository, ConnectCallRepository
)
from src.modules.connect.models import ConnectChannel, ConnectTemplate, ConnectMessage, ConnectCall
from src.modules.connect.schemas import (
    ConnectChannelSchema, ConnectTemplateSchema, 
    ConnectMessageSchema, ConnectCallSchema
)

class ConnectChannelService:
    def __init__(self, repo: ConnectChannelRepository):
        self.repo = repo

    def create_channel(self, schema: ConnectChannelSchema) -> ConnectChannelSchema:
        channel = ConnectChannel(**schema.dict(exclude_unset=True))
        created = self.repo.create(channel)
        return ConnectChannelSchema.from_orm(created)

    def get_channel(self, channel_id: int) -> Optional[ConnectChannelSchema]:
        channel = self.repo.get_by_id(channel_id)
        return ConnectChannelSchema.from_orm(channel) if channel else None

    def get_by_code(self, code: str) -> Optional[ConnectChannelSchema]:
        channel = self.repo.get_by_code(code)
        return ConnectChannelSchema.from_orm(channel) if channel else None

    def list_channels(self, active_only: bool = True) -> List[ConnectChannelSchema]:
        channels = self.repo.list_all(active_only)
        return [ConnectChannelSchema.from_orm(c) for c in channels]

    def update_channel(self, channel_id: int, schema: ConnectChannelSchema) -> Optional[ConnectChannelSchema]:
        updated = self.repo.update(channel_id, **schema.dict(exclude_unset=True))
        return ConnectChannelSchema.from_orm(updated) if updated else None

    def delete_channel(self, channel_id: int) -> bool:
        return self.repo.delete(channel_id)

class ConnectTemplateService:
    def __init__(self, repo: ConnectTemplateRepository):
        self.repo = repo

    def create_template(self, schema: ConnectTemplateSchema) -> ConnectTemplateSchema:
        template = ConnectTemplate(**schema.dict(exclude_unset=True))
        created = self.repo.create(template)
        return ConnectTemplateSchema.from_orm(created)

    def get_template(self, template_id: int) -> Optional[ConnectTemplateSchema]:
        template = self.repo.get_by_id(template_id)
        return ConnectTemplateSchema.from_orm(template) if template else None

    def list_by_type(self, template_type: str, published_only: bool = True) -> List[ConnectTemplateSchema]:
        templates = self.repo.list_by_type(template_type, published_only)
        return [ConnectTemplateSchema.from_orm(t) for t in templates]

    def list_by_category(self, category: str) -> List[ConnectTemplateSchema]:
        templates = self.repo.list_by_category(category)
        return [ConnectTemplateSchema.from_orm(t) for t in templates]

    def list_all_templates(self, limit: int = 100, published_only: bool = False) -> List[ConnectTemplateSchema]:
        templates = self.repo.list_all(limit, published_only)
        return [ConnectTemplateSchema.from_orm(t) for t in templates]

    def update_template(self, template_id: int, schema: ConnectTemplateSchema) -> Optional[ConnectTemplateSchema]:
        updated = self.repo.update(template_id, **schema.dict(exclude_unset=True))
        return ConnectTemplateSchema.from_orm(updated) if updated else None

    def delete_template(self, template_id: int) -> bool:
        return self.repo.delete(template_id)

    def use_template(self, template_id: int) -> None:
        self.repo.increment_usage(template_id)

class ConnectMessageService:
    def __init__(self, repo: ConnectMessageRepository):
        self.repo = repo

    def create_message(self, schema: ConnectMessageSchema) -> ConnectMessageSchema:
        message = ConnectMessage(**schema.dict(exclude_unset=True))
        created = self.repo.create(message)
        return ConnectMessageSchema.from_orm(created)

    def get_message(self, message_id: int) -> Optional[ConnectMessageSchema]:
        message = self.repo.get_by_id(message_id)
        return ConnectMessageSchema.from_orm(message) if message else None

    def list_all_messages(self, limit: int = 100, skip: int = 0) -> List[ConnectMessageSchema]:
        messages = self.repo.list_all(limit, skip)
        return [ConnectMessageSchema.from_orm(m) for m in messages]

    def list_user_messages(self, user_id: int, limit: int = 20) -> List[ConnectMessageSchema]:
        messages = self.repo.list_by_user(user_id, limit)
        return [ConnectMessageSchema.from_orm(m) for m in messages]

    def list_by_status(self, status: str, limit: int = 20) -> List[ConnectMessageSchema]:
        messages = self.repo.list_by_status(status, limit)
        return [ConnectMessageSchema.from_orm(m) for m in messages]

    def get_thread(self, thread_id: str) -> List[ConnectMessageSchema]:
        messages = self.repo.list_by_thread(thread_id)
        return [ConnectMessageSchema.from_orm(m) for m in messages]

    def update_message(self, message_id: int, schema: ConnectMessageSchema) -> Optional[ConnectMessageSchema]:
        updated = self.repo.update(message_id, **schema.dict(exclude_unset=True))
        return ConnectMessageSchema.from_orm(updated) if updated else None

    def send_message(self, message_id: int) -> Optional[ConnectMessageSchema]:
        message = self.repo.mark_as_sent(message_id)
        return ConnectMessageSchema.from_orm(message) if message else None

    def track_open(self, message_id: int) -> Optional[ConnectMessageSchema]:
        message = self.repo.mark_as_opened(message_id)
        return ConnectMessageSchema.from_orm(message) if message else None

    def track_click(self, message_id: int) -> Optional[ConnectMessageSchema]:
        message = self.repo.mark_as_clicked(message_id)
        return ConnectMessageSchema.from_orm(message) if message else None

    def archive_message(self, message_id: int) -> Optional[ConnectMessageSchema]:
        message = self.repo.archive(message_id)
        return ConnectMessageSchema.from_orm(message) if message else None

class ConnectCallService:
    def __init__(self, repo: ConnectCallRepository):
        self.repo = repo

    def create_call(self, schema: ConnectCallSchema) -> ConnectCallSchema:
        call = ConnectCall(**schema.dict(exclude_unset=True))
        created = self.repo.create(call)
        return ConnectCallSchema.from_orm(created)

    def get_call(self, call_id: int) -> Optional[ConnectCallSchema]:
        call = self.repo.get_by_id(call_id)
        return ConnectCallSchema.from_orm(call) if call else None

    def get_by_sid(self, call_sid: str) -> Optional[ConnectCallSchema]:
        call = self.repo.get_by_sid(call_sid)
        return ConnectCallSchema.from_orm(call) if call else None

    def list_user_calls(self, user_id: int, limit: int = 20) -> List[ConnectCallSchema]:
        calls = self.repo.list_by_user(user_id, limit)
        return [ConnectCallSchema.from_orm(c) for c in calls]

    def list_by_status(self, status: str, limit: int = 20) -> List[ConnectCallSchema]:
        calls = self.repo.list_by_status(status, limit)
        return [ConnectCallSchema.from_orm(c) for c in calls]

    def update_call(self, call_id: int, schema: ConnectCallSchema) -> Optional[ConnectCallSchema]:
        updated = self.repo.update(call_id, **schema.dict(exclude_unset=True))
        return ConnectCallSchema.from_orm(updated) if updated else None

    def get_pending_followups(self) -> List[ConnectCallSchema]:
        calls = self.repo.list_pending_followup()
        return [ConnectCallSchema.from_orm(c) for c in calls]
