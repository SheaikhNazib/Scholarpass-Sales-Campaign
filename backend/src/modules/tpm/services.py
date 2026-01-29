from typing import Optional, List
from src.modules.tpm.repositories import (
    TPMTaskStatusRepository, TPMProjectStatusRepository, TPMTagRepository,
    TPMProjectRepository, TPMTaskEventRepository, TPMAIAgentRuleRepository,
    TPMAIAgentConversationRepository
)
from src.modules.tpm.models import (
    TPMTaskStatus, TPMProjectStatus, TPMTag, TPMProject, TPMTaskEvent,
    TPMAIAgentRule, TPMAIAgentConversation
)
from src.modules.tpm.schemas import (
    TPMTaskStatusSchema, TPMProjectStatusSchema, TPMTagSchema,
    TPMProjectSchema, TPMTaskEventSchema, TPMAIAgentRuleSchema,
    TPMAIAgentConversationSchema
)

class TPMStatusService:
    def __init__(self, repo):
        self.repo = repo

    def create_status(self, schema) -> any:
        status = self.repo.create(schema)
        return status

    def get_status(self, status_id: int) -> Optional[any]:
        return self.repo.get_by_id(status_id)

    def list_statuses(self) -> List[any]:
        return self.repo.list_all()

    def update_status(self, status_id: int, schema) -> Optional[any]:
        return self.repo.update(status_id, **schema.dict(exclude_unset=True))

    def delete_status(self, status_id: int) -> bool:
        return self.repo.delete(status_id)

class TPMProjectService:
    def __init__(self, repo: TPMProjectRepository):
        self.repo = repo

    def create_project(self, schema: TPMProjectSchema) -> TPMProjectSchema:
        project = TPMProject(**schema.dict(exclude_unset=True))
        created = self.repo.create(project)
        return TPMProjectSchema.from_orm(created)

    def get_project(self, project_id: int) -> Optional[TPMProjectSchema]:
        project = self.repo.get_by_id(project_id)
        return TPMProjectSchema.from_orm(project) if project else None

    def list_by_manager(self, manager_id: int, limit: int = 20) -> List[TPMProjectSchema]:
        projects = self.repo.list_by_manager(manager_id, limit)
        return [TPMProjectSchema.from_orm(p) for p in projects]

    def list_active(self, limit: int = 20) -> List[TPMProjectSchema]:
        projects = self.repo.list_active(limit)
        return [TPMProjectSchema.from_orm(p) for p in projects]

    def update_project(self, project_id: int, schema: TPMProjectSchema) -> Optional[TPMProjectSchema]:
        updated = self.repo.update(project_id, **schema.dict(exclude_unset=True))
        return TPMProjectSchema.from_orm(updated) if updated else None

    def delete_project(self, project_id: int) -> bool:
        return self.repo.delete(project_id)

class TPMTaskEventService:
    def __init__(self, repo: TPMTaskEventRepository):
        self.repo = repo

    def create_task(self, schema: TPMTaskEventSchema) -> TPMTaskEventSchema:
        task = TPMTaskEvent(**schema.dict(exclude_unset=True))
        created = self.repo.create(task)
        return TPMTaskEventSchema.from_orm(created)

    def get_task(self, task_id: int) -> Optional[TPMTaskEventSchema]:
        task = self.repo.get_by_id(task_id)
        return TPMTaskEventSchema.from_orm(task) if task else None

    def list_by_project(self, project_id: int, limit: int = 20) -> List[TPMTaskEventSchema]:
        tasks = self.repo.list_by_project(project_id, limit)
        return [TPMTaskEventSchema.from_orm(t) for t in tasks]

    def list_by_assignee(self, user_id: int, limit: int = 20) -> List[TPMTaskEventSchema]:
        tasks = self.repo.list_by_assignee(user_id, limit)
        return [TPMTaskEventSchema.from_orm(t) for t in tasks]

    def list_by_status(self, status_id: int, limit: int = 20) -> List[TPMTaskEventSchema]:
        tasks = self.repo.list_by_status(status_id, limit)
        return [TPMTaskEventSchema.from_orm(t) for t in tasks]

    def update_task(self, task_id: int, schema: TPMTaskEventSchema) -> Optional[TPMTaskEventSchema]:
        updated = self.repo.update(task_id, **schema.dict(exclude_unset=True))
        return TPMTaskEventSchema.from_orm(updated) if updated else None

    def complete_task(self, task_id: int) -> Optional[TPMTaskEventSchema]:
        completed = self.repo.mark_completed(task_id)
        return TPMTaskEventSchema.from_orm(completed) if completed else None

class TPMAIAgentRuleService:
    def __init__(self, repo: TPMAIAgentRuleRepository):
        self.repo = repo

    def create_rule(self, schema: TPMAIAgentRuleSchema) -> TPMAIAgentRuleSchema:
        rule = TPMAIAgentRule(**schema.dict(exclude_unset=True))
        created = self.repo.create(rule)
        return TPMAIAgentRuleSchema.from_orm(created)

    def get_rule(self, rule_id: int) -> Optional[TPMAIAgentRuleSchema]:
        rule = self.repo.get_by_id(rule_id)
        return TPMAIAgentRuleSchema.from_orm(rule) if rule else None

    def list_active_rules(self) -> List[TPMAIAgentRuleSchema]:
        rules = self.repo.list_active()
        return [TPMAIAgentRuleSchema.from_orm(r) for r in rules]

    def list_by_trigger(self, trigger_type: str) -> List[TPMAIAgentRuleSchema]:
        rules = self.repo.list_by_trigger(trigger_type)
        return [TPMAIAgentRuleSchema.from_orm(r) for r in rules]

    def update_rule(self, rule_id: int, schema: TPMAIAgentRuleSchema) -> Optional[TPMAIAgentRuleSchema]:
        updated = self.repo.update(rule_id, **schema.dict(exclude_unset=True))
        return TPMAIAgentRuleSchema.from_orm(updated) if updated else None

class TPMAIAgentConversationService:
    def __init__(self, repo: TPMAIAgentConversationRepository):
        self.repo = repo

    def create_conversation(self, schema: TPMAIAgentConversationSchema) -> TPMAIAgentConversationSchema:
        conversation = TPMAIAgentConversation(**schema.dict(exclude_unset=True))
        created = self.repo.create(conversation)
        return TPMAIAgentConversationSchema.from_orm(created)

    def get_conversation(self, conversation_id: int) -> Optional[TPMAIAgentConversationSchema]:
        conversation = self.repo.get_by_id(conversation_id)
        return TPMAIAgentConversationSchema.from_orm(conversation) if conversation else None

    def list_by_task(self, task_id: int, limit: int = 20) -> List[TPMAIAgentConversationSchema]:
        conversations = self.repo.list_by_task(task_id, limit)
        return [TPMAIAgentConversationSchema.from_orm(c) for c in conversations]

    def get_pending_followups(self) -> List[TPMAIAgentConversationSchema]:
        conversations = self.repo.list_pending_followup()
        return [TPMAIAgentConversationSchema.from_orm(c) for c in conversations]

    def get_pending_escalations(self) -> List[TPMAIAgentConversationSchema]:
        conversations = self.repo.list_pending_escalation()
        return [TPMAIAgentConversationSchema.from_orm(c) for c in conversations]

    def update_conversation(self, conversation_id: int, schema: TPMAIAgentConversationSchema) -> Optional[TPMAIAgentConversationSchema]:
        updated = self.repo.update(conversation_id, **schema.dict(exclude_unset=True))
        return TPMAIAgentConversationSchema.from_orm(updated) if updated else None
