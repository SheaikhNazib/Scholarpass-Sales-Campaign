from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.modules.tpm.services import (
    TPMStatusService, TPMProjectService, TPMTaskEventService,
    TPMAIAgentRuleService, TPMAIAgentConversationService
)
from src.modules.tpm.repositories import (
    TPMTaskStatusRepository, TPMProjectStatusRepository, TPMTagRepository,
    TPMProjectRepository, TPMTaskEventRepository, TPMAIAgentRuleRepository,
    TPMAIAgentConversationRepository
)
from src.modules.tpm.schemas import (
    TPMTaskStatusSchema, TPMProjectStatusSchema, TPMTagSchema,
    TPMProjectSchema, TPMTaskEventSchema, TPMAIAgentRuleSchema,
    TPMAIAgentConversationSchema
)

router = APIRouter(prefix="/api/tpm", tags=["tpm"])

def get_task_status_service(db: Session = Depends(get_db)) -> TPMStatusService:
    return TPMStatusService(TPMTaskStatusRepository(db))

def get_project_status_service(db: Session = Depends(get_db)) -> TPMStatusService:
    return TPMStatusService(TPMProjectStatusRepository(db))

def get_tag_service(db: Session = Depends(get_db)) -> TPMStatusService:
    return TPMStatusService(TPMTagRepository(db))

def get_project_service(db: Session = Depends(get_db)) -> TPMProjectService:
    return TPMProjectService(TPMProjectRepository(db))

def get_task_service(db: Session = Depends(get_db)) -> TPMTaskEventService:
    return TPMTaskEventService(TPMTaskEventRepository(db))

def get_ai_rule_service(db: Session = Depends(get_db)) -> TPMAIAgentRuleService:
    return TPMAIAgentRuleService(TPMAIAgentRuleRepository(db))

def get_ai_conversation_service(db: Session = Depends(get_db)) -> TPMAIAgentConversationService:
    return TPMAIAgentConversationService(TPMAIAgentConversationRepository(db))

@router.post("/task-statuses", response_model=TPMTaskStatusSchema, status_code=status.HTTP_201_CREATED)
def create_task_status(schema: TPMTaskStatusSchema, service: TPMStatusService = Depends(get_task_status_service)):
    return service.create_status(schema)

@router.get("/task-statuses", response_model=list[TPMTaskStatusSchema])
def list_task_statuses(service: TPMStatusService = Depends(get_task_status_service)):
    return service.list_statuses()

@router.get("/task-statuses/{status_id}", response_model=TPMTaskStatusSchema)
def get_task_status(status_id: int, service: TPMStatusService = Depends(get_task_status_service)):
    status = service.get_status(status_id)
    if not status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Status not found")
    return status

@router.put("/task-statuses/{status_id}", response_model=TPMTaskStatusSchema)
def update_task_status(status_id: int, schema: TPMTaskStatusSchema, service: TPMStatusService = Depends(get_task_status_service)):
    updated = service.update_status(status_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Status not found")
    return updated

@router.delete("/task-statuses/{status_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_status(status_id: int, service: TPMStatusService = Depends(get_task_status_service)):
    if not service.delete_status(status_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Status not found")

@router.post("/project-statuses", response_model=TPMProjectStatusSchema, status_code=status.HTTP_201_CREATED)
def create_project_status(schema: TPMProjectStatusSchema, service: TPMStatusService = Depends(get_project_status_service)):
    return service.create_status(schema)

@router.get("/project-statuses", response_model=list[TPMProjectStatusSchema])
def list_project_statuses(service: TPMStatusService = Depends(get_project_status_service)):
    return service.list_statuses()

@router.post("/tags", response_model=TPMTagSchema, status_code=status.HTTP_201_CREATED)
def create_tag(schema: TPMTagSchema, service: TPMStatusService = Depends(get_tag_service)):
    return service.create_status(schema)

@router.get("/tags", response_model=list[TPMTagSchema])
def list_tags(service: TPMStatusService = Depends(get_tag_service)):
    return service.list_statuses()

@router.post("/projects", response_model=TPMProjectSchema, status_code=status.HTTP_201_CREATED)
def create_project(schema: TPMProjectSchema, service: TPMProjectService = Depends(get_project_service)):
    return service.create_project(schema)

@router.get("/projects/{project_id}", response_model=TPMProjectSchema)
def get_project(project_id: int, service: TPMProjectService = Depends(get_project_service)):
    project = service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project

@router.get("/projects/manager/{manager_id}", response_model=list[TPMProjectSchema])
def list_projects_by_manager(manager_id: int, limit: int = 20, service: TPMProjectService = Depends(get_project_service)):
    return service.list_by_manager(manager_id, limit)

@router.get("/projects", response_model=list[TPMProjectSchema])
def list_active_projects(limit: int = 20, service: TPMProjectService = Depends(get_project_service)):
    return service.list_active(limit)

@router.put("/projects/{project_id}", response_model=TPMProjectSchema)
def update_project(project_id: int, schema: TPMProjectSchema, service: TPMProjectService = Depends(get_project_service)):
    updated = service.update_project(project_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return updated

@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, service: TPMProjectService = Depends(get_project_service)):
    if not service.delete_project(project_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

@router.post("/tasks", response_model=TPMTaskEventSchema, status_code=status.HTTP_201_CREATED)
def create_task(schema: TPMTaskEventSchema, service: TPMTaskEventService = Depends(get_task_service)):
    return service.create_task(schema)

@router.get("/tasks/{task_id}", response_model=TPMTaskEventSchema)
def get_task(task_id: int, service: TPMTaskEventService = Depends(get_task_service)):
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.get("/tasks/project/{project_id}", response_model=list[TPMTaskEventSchema])
def list_tasks_by_project(project_id: int, limit: int = 20, service: TPMTaskEventService = Depends(get_task_service)):
    return service.list_by_project(project_id, limit)

@router.get("/tasks/assignee/{user_id}", response_model=list[TPMTaskEventSchema])
def list_tasks_by_assignee(user_id: int, limit: int = 20, service: TPMTaskEventService = Depends(get_task_service)):
    return service.list_by_assignee(user_id, limit)

@router.get("/tasks/status/{status_id}", response_model=list[TPMTaskEventSchema])
def list_tasks_by_status(status_id: int, limit: int = 20, service: TPMTaskEventService = Depends(get_task_service)):
    return service.list_by_status(status_id, limit)

@router.put("/tasks/{task_id}", response_model=TPMTaskEventSchema)
def update_task(task_id: int, schema: TPMTaskEventSchema, service: TPMTaskEventService = Depends(get_task_service)):
    updated = service.update_task(task_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return updated

@router.post("/tasks/{task_id}/complete", response_model=TPMTaskEventSchema)
def complete_task(task_id: int, service: TPMTaskEventService = Depends(get_task_service)):
    completed = service.complete_task(task_id)
    if not completed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return completed

@router.post("/ai-rules", response_model=TPMAIAgentRuleSchema, status_code=status.HTTP_201_CREATED)
def create_ai_rule(schema: TPMAIAgentRuleSchema, service: TPMAIAgentRuleService = Depends(get_ai_rule_service)):
    return service.create_rule(schema)

@router.get("/ai-rules/{rule_id}", response_model=TPMAIAgentRuleSchema)
def get_ai_rule(rule_id: int, service: TPMAIAgentRuleService = Depends(get_ai_rule_service)):
    rule = service.get_rule(rule_id)
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")
    return rule

@router.get("/ai-rules", response_model=list[TPMAIAgentRuleSchema])
def list_active_ai_rules(service: TPMAIAgentRuleService = Depends(get_ai_rule_service)):
    return service.list_active_rules()

@router.get("/ai-rules/trigger/{trigger_type}", response_model=list[TPMAIAgentRuleSchema])
def list_ai_rules_by_trigger(trigger_type: str, service: TPMAIAgentRuleService = Depends(get_ai_rule_service)):
    return service.list_by_trigger(trigger_type)

@router.put("/ai-rules/{rule_id}", response_model=TPMAIAgentRuleSchema)
def update_ai_rule(rule_id: int, schema: TPMAIAgentRuleSchema, service: TPMAIAgentRuleService = Depends(get_ai_rule_service)):
    updated = service.update_rule(rule_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")
    return updated

@router.post("/ai-conversations", response_model=TPMAIAgentConversationSchema, status_code=status.HTTP_201_CREATED)
def create_ai_conversation(schema: TPMAIAgentConversationSchema, service: TPMAIAgentConversationService = Depends(get_ai_conversation_service)):
    return service.create_conversation(schema)

@router.get("/ai-conversations/{conversation_id}", response_model=TPMAIAgentConversationSchema)
def get_ai_conversation(conversation_id: int, service: TPMAIAgentConversationService = Depends(get_ai_conversation_service)):
    conversation = service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return conversation

@router.get("/ai-conversations/task/{task_id}", response_model=list[TPMAIAgentConversationSchema])
def list_ai_conversations_by_task(task_id: int, limit: int = 20, service: TPMAIAgentConversationService = Depends(get_ai_conversation_service)):
    return service.list_by_task(task_id, limit)

@router.get("/ai-conversations/pending-followup", response_model=list[TPMAIAgentConversationSchema])
def get_pending_followups(service: TPMAIAgentConversationService = Depends(get_ai_conversation_service)):
    return service.get_pending_followups()

@router.get("/ai-conversations/pending-escalation", response_model=list[TPMAIAgentConversationSchema])
def get_pending_escalations(service: TPMAIAgentConversationService = Depends(get_ai_conversation_service)):
    return service.get_pending_escalations()

@router.put("/ai-conversations/{conversation_id}", response_model=TPMAIAgentConversationSchema)
def update_ai_conversation(conversation_id: int, schema: TPMAIAgentConversationSchema, service: TPMAIAgentConversationService = Depends(get_ai_conversation_service)):
    updated = service.update_conversation(conversation_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return updated
