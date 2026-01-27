from typing import Optional, List, Protocol
from sqlalchemy.orm import Session
from datetime import datetime
from src.modules.tpm.models import (
    TPMTaskStatus, TPMProjectStatus, TPMTag, TPMProject, TPMTaskEvent,
    TPMProjectTeam, TPMProjectNote, TPMTaskWorkItem, TPMAIAgentRule, TPMAIAgentConversation
)

class ITPMStatusRepository(Protocol):
    def create(self, status) -> any: ...
    def get_by_id(self, status_id: int) -> Optional[any]: ...
    def list_all(self) -> List[any]: ...
    def update(self, status_id: int, **kwargs) -> Optional[any]: ...
    def delete(self, status_id: int) -> bool: ...

class ITPMProjectRepository(Protocol):
    def create(self, project: TPMProject) -> TPMProject: ...
    def get_by_id(self, project_id: int) -> Optional[TPMProject]: ...
    def list_by_manager(self, manager_id: int, limit: int = 20) -> List[TPMProject]: ...
    def list_active(self, limit: int = 20) -> List[TPMProject]: ...
    def update(self, project_id: int, **kwargs) -> Optional[TPMProject]: ...
    def delete(self, project_id: int) -> bool: ...

class ITPMTaskEventRepository(Protocol):
    def create(self, task: TPMTaskEvent) -> TPMTaskEvent: ...
    def get_by_id(self, task_id: int) -> Optional[TPMTaskEvent]: ...
    def list_by_project(self, project_id: int, limit: int = 20) -> List[TPMTaskEvent]: ...
    def list_by_assignee(self, user_id: int, limit: int = 20) -> List[TPMTaskEvent]: ...
    def list_by_status(self, status_id: int, limit: int = 20) -> List[TPMTaskEvent]: ...
    def update(self, task_id: int, **kwargs) -> Optional[TPMTaskEvent]: ...
    def mark_completed(self, task_id: int) -> Optional[TPMTaskEvent]: ...

class ITPMAIAgentRuleRepository(Protocol):
    def create(self, rule: TPMAIAgentRule) -> TPMAIAgentRule: ...
    def get_by_id(self, rule_id: int) -> Optional[TPMAIAgentRule]: ...
    def list_active(self) -> List[TPMAIAgentRule]: ...
    def list_by_trigger(self, trigger_type: str) -> List[TPMAIAgentRule]: ...
    def update(self, rule_id: int, **kwargs) -> Optional[TPMAIAgentRule]: ...

class ITPMAIConversationRepository(Protocol):
    def create(self, conversation: TPMAIAgentConversation) -> TPMAIAgentConversation: ...
    def get_by_id(self, conversation_id: int) -> Optional[TPMAIAgentConversation]: ...
    def list_by_task(self, task_id: int, limit: int = 20) -> List[TPMAIAgentConversation]: ...
    def list_pending_followup(self) -> List[TPMAIAgentConversation]: ...
    def list_pending_escalation(self) -> List[TPMAIAgentConversation]: ...
    def update(self, conversation_id: int, **kwargs) -> Optional[TPMAIAgentConversation]: ...

class TPMTaskStatusRepository(ITPMStatusRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, status: TPMTaskStatus) -> TPMTaskStatus:
        self.db.add(status)
        self.db.commit()
        self.db.refresh(status)
        return status

    def get_by_id(self, status_id: int) -> Optional[TPMTaskStatus]:
        return self.db.query(TPMTaskStatus).filter(TPMTaskStatus.id == status_id).first()

    def list_all(self) -> List[TPMTaskStatus]:
        return self.db.query(TPMTaskStatus).order_by(TPMTaskStatus.display_sequence).all()

    def update(self, status_id: int, **kwargs) -> Optional[TPMTaskStatus]:
        status = self.get_by_id(status_id)
        if status:
            for key, value in kwargs.items():
                setattr(status, key, value)
            self.db.commit()
            self.db.refresh(status)
        return status

    def delete(self, status_id: int) -> bool:
        status = self.get_by_id(status_id)
        if status:
            self.db.delete(status)
            self.db.commit()
            return True
        return False

class TPMProjectStatusRepository(ITPMStatusRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, status: TPMProjectStatus) -> TPMProjectStatus:
        self.db.add(status)
        self.db.commit()
        self.db.refresh(status)
        return status

    def get_by_id(self, status_id: int) -> Optional[TPMProjectStatus]:
        return self.db.query(TPMProjectStatus).filter(TPMProjectStatus.id == status_id).first()

    def list_all(self) -> List[TPMProjectStatus]:
        return self.db.query(TPMProjectStatus).order_by(TPMProjectStatus.display_sequence).all()

    def update(self, status_id: int, **kwargs) -> Optional[TPMProjectStatus]:
        status = self.get_by_id(status_id)
        if status:
            for key, value in kwargs.items():
                setattr(status, key, value)
            self.db.commit()
            self.db.refresh(status)
        return status

    def delete(self, status_id: int) -> bool:
        status = self.get_by_id(status_id)
        if status:
            self.db.delete(status)
            self.db.commit()
            return True
        return False

class TPMTagRepository(ITPMStatusRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, tag: TPMTag) -> TPMTag:
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def get_by_id(self, tag_id: int) -> Optional[TPMTag]:
        return self.db.query(TPMTag).filter(TPMTag.id == tag_id).first()

    def list_all(self) -> List[TPMTag]:
        return self.db.query(TPMTag).all()

    def update(self, tag_id: int, **kwargs) -> Optional[TPMTag]:
        tag = self.get_by_id(tag_id)
        if tag:
            for key, value in kwargs.items():
                setattr(tag, key, value)
            self.db.commit()
            self.db.refresh(tag)
        return tag

    def delete(self, tag_id: int) -> bool:
        tag = self.get_by_id(tag_id)
        if tag:
            self.db.delete(tag)
            self.db.commit()
            return True
        return False

class TPMProjectRepository(ITPMProjectRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, project: TPMProject) -> TPMProject:
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_by_id(self, project_id: int) -> Optional[TPMProject]:
        return self.db.query(TPMProject).filter(TPMProject.id == project_id).first()

    def list_by_manager(self, manager_id: int, limit: int = 20) -> List[TPMProject]:
        return self.db.query(TPMProject).filter(
            TPMProject.project_manager_user_id == manager_id
        ).order_by(TPMProject.created_at.desc()).limit(limit).all()

    def list_active(self, limit: int = 20) -> List[TPMProject]:
        return self.db.query(TPMProject).filter(
            TPMProject.is_active == True,
            TPMProject.is_archived == False
        ).order_by(TPMProject.created_at.desc()).limit(limit).all()

    def update(self, project_id: int, **kwargs) -> Optional[TPMProject]:
        project = self.get_by_id(project_id)
        if project:
            for key, value in kwargs.items():
                setattr(project, key, value)
            self.db.commit()
            self.db.refresh(project)
        return project

    def delete(self, project_id: int) -> bool:
        project = self.get_by_id(project_id)
        if project:
            self.db.delete(project)
            self.db.commit()
            return True
        return False

class TPMTaskEventRepository(ITPMTaskEventRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, task: TPMTaskEvent) -> TPMTaskEvent:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: int) -> Optional[TPMTaskEvent]:
        return self.db.query(TPMTaskEvent).filter(TPMTaskEvent.id == task_id).first()

    def list_by_project(self, project_id: int, limit: int = 20) -> List[TPMTaskEvent]:
        return self.db.query(TPMTaskEvent).filter(
            TPMTaskEvent.tpm_project_id == project_id
        ).order_by(TPMTaskEvent.created_at.desc()).limit(limit).all()

    def list_by_assignee(self, user_id: int, limit: int = 20) -> List[TPMTaskEvent]:
        return self.db.query(TPMTaskEvent).filter(
            TPMTaskEvent.assigned_to_user_id == user_id
        ).order_by(TPMTaskEvent.created_at.desc()).limit(limit).all()

    def list_by_status(self, status_id: int, limit: int = 20) -> List[TPMTaskEvent]:
        return self.db.query(TPMTaskEvent).filter(
            TPMTaskEvent.tpm_master_task_status_id == status_id
        ).order_by(TPMTaskEvent.created_at.desc()).limit(limit).all()

    def update(self, task_id: int, **kwargs) -> Optional[TPMTaskEvent]:
        task = self.get_by_id(task_id)
        if task:
            for key, value in kwargs.items():
                setattr(task, key, value)
            self.db.commit()
            self.db.refresh(task)
        return task

    def mark_completed(self, task_id: int) -> Optional[TPMTaskEvent]:
        return self.update(task_id, is_completed=True, completed_at=datetime.utcnow())

class TPMAIAgentRuleRepository(ITPMAIAgentRuleRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, rule: TPMAIAgentRule) -> TPMAIAgentRule:
        self.db.add(rule)
        self.db.commit()
        self.db.refresh(rule)
        return rule

    def get_by_id(self, rule_id: int) -> Optional[TPMAIAgentRule]:
        return self.db.query(TPMAIAgentRule).filter(TPMAIAgentRule.id == rule_id).first()

    def list_active(self) -> List[TPMAIAgentRule]:
        return self.db.query(TPMAIAgentRule).filter(TPMAIAgentRule.is_active == True).all()

    def list_by_trigger(self, trigger_type: str) -> List[TPMAIAgentRule]:
        return self.db.query(TPMAIAgentRule).filter(
            TPMAIAgentRule.trigger_type == trigger_type,
            TPMAIAgentRule.is_active == True
        ).all()

    def update(self, rule_id: int, **kwargs) -> Optional[TPMAIAgentRule]:
        rule = self.get_by_id(rule_id)
        if rule:
            for key, value in kwargs.items():
                setattr(rule, key, value)
            self.db.commit()
            self.db.refresh(rule)
        return rule

class TPMAIAgentConversationRepository(ITPMAIConversationRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, conversation: TPMAIAgentConversation) -> TPMAIAgentConversation:
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def get_by_id(self, conversation_id: int) -> Optional[TPMAIAgentConversation]:
        return self.db.query(TPMAIAgentConversation).filter(TPMAIAgentConversation.id == conversation_id).first()

    def list_by_task(self, task_id: int, limit: int = 20) -> List[TPMAIAgentConversation]:
        return self.db.query(TPMAIAgentConversation).filter(
            TPMAIAgentConversation.tpm_task_event_id == task_id
        ).order_by(TPMAIAgentConversation.created_at.desc()).limit(limit).all()

    def list_pending_followup(self) -> List[TPMAIAgentConversation]:
        return self.db.query(TPMAIAgentConversation).filter(
            TPMAIAgentConversation.requires_follow_up == True,
            TPMAIAgentConversation.follow_up_at <= datetime.utcnow()
        ).all()

    def list_pending_escalation(self) -> List[TPMAIAgentConversation]:
        return self.db.query(TPMAIAgentConversation).filter(
            TPMAIAgentConversation.escalate_to_manager == True,
            TPMAIAgentConversation.escalated_at == None
        ).all()

    def update(self, conversation_id: int, **kwargs) -> Optional[TPMAIAgentConversation]:
        conversation = self.get_by_id(conversation_id)
        if conversation:
            for key, value in kwargs.items():
                setattr(conversation, key, value)
            self.db.commit()
            self.db.refresh(conversation)
        return conversation
