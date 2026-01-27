from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date

class TPMTaskStatusSchema(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=128)
    color_code: Optional[str] = None
    display_sequence: Optional[int] = None
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TPMProjectStatusSchema(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=128)
    color_code: Optional[str] = None
    display_sequence: Optional[int] = None
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TPMTagSchema(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=128)
    color_code: Optional[str] = None
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TPMProjectSchema(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=1024)
    project_code: Optional[str] = None
    tpm_master_project_status_id: Optional[int] = None
    task_project_tags: Optional[Dict[str, Any]] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    actual_start_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    number_of_hours: Optional[int] = None
    number_of_working_days: Optional[int] = None
    number_of_team_members: Optional[int] = None
    number_of_milestones_tasks: Optional[int] = None
    milestones_status: Optional[int] = None
    progress_percentage: int = 0
    timeline_status: Optional[str] = None
    brief: Optional[str] = None
    detailed_description: Optional[str] = None
    estimated_budget: Optional[float] = None
    actual_budget: Optional[float] = None
    master_currency_id: Optional[int] = None
    project_manager_user_id: Optional[int] = None
    project_owner_user_id: Optional[int] = None
    is_active: bool = True
    is_archived: bool = False
    archived_at: Optional[datetime] = None
    master_hub_id: Optional[int] = None
    company_id: Optional[int] = None
    institute_id: Optional[int] = None
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TPMTaskEventSchema(BaseModel):
    id: Optional[int] = None
    tpm_project_id: Optional[int] = None
    task_or_event: bool
    name: str = Field(..., min_length=1, max_length=2048)
    description: Optional[str] = None
    tpm_master_task_status_id: Optional[int] = None
    priority: Optional[str] = None
    progress: int = 0
    start_date_time: Optional[datetime] = None
    end_date_time: Optional[datetime] = None
    estimated_time_in_hours: Optional[float] = None
    actual_time_in_hours: Optional[float] = None
    assigned_to_user_id: Optional[int] = None
    assigned_to_employee_id: Optional[int] = None
    save_as_template: bool = False
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None
    tags: Optional[List[str]] = None
    is_completed: bool = False
    completed_at: Optional[datetime] = None
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    deleted_by_user_id: Optional[int] = None
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TPMProjectTeamSchema(BaseModel):
    id: Optional[int] = None
    tpm_project_id: int
    app_user_id: Optional[int] = None
    crm_contact_id: Optional[int] = None
    full_name: Optional[str] = None
    job_title: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    responsibilities: Optional[str] = None
    allocation_percentage: Optional[int] = None
    daily_work_hours: Optional[float] = None
    is_active: bool = True
    joined_date: Optional[date] = None
    left_date: Optional[date] = None
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TPMProjectNoteSchema(BaseModel):
    id: Optional[int] = None
    tpm_project_id: int
    parent_note_id: Optional[int] = None
    notes: Optional[str] = None
    note_type: str = 'general'
    has_attachments: bool = False
    attachments: Optional[Dict[str, Any]] = None
    linked_document_ids: Optional[List[int]] = None
    is_pinned: bool = False
    pinned_at: Optional[datetime] = None
    pinned_by_user_id: Optional[int] = None
    reply_count: int = 0
    like_count: int = 0
    reactions: Optional[Dict[str, Any]] = None
    is_edited: bool = False
    edited_at: Optional[datetime] = None
    edit_history: Optional[Dict[str, Any]] = None
    mentioned_user_ids: Optional[List[int]] = None
    notification_sent: bool = False
    read_by_user_ids: Optional[List[int]] = None
    is_important: bool = False
    priority: Optional[str] = None
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    deleted_by_user_id: Optional[int] = None
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TPMTaskWorkItemSchema(BaseModel):
    id: Optional[int] = None
    tpm_task_event_id: int
    name: str = Field(..., min_length=1, max_length=1024)
    description: Optional[str] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    start_date_time: Optional[datetime] = None
    end_date_time: Optional[datetime] = None
    open_or_closed: bool = True
    completed_at: Optional[datetime] = None
    assigned_to_user_id: Optional[int] = None
    assign_dated_time: Optional[datetime] = None
    assigned_to_contact_id: Optional[int] = None
    display_sequence: Optional[int] = None
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TPMAIAgentRuleSchema(BaseModel):
    id: Optional[int] = None
    rule_name: str = Field(..., min_length=1, max_length=256)
    description: Optional[str] = None
    trigger_type: str = Field(..., pattern="^(task_overdue|task_due_soon|no_update|status_change|project_milestone)$")
    days_before_due: Optional[int] = None
    hours_after_overdue: Optional[int] = None
    days_without_update: Optional[int] = None
    ai_model: str = "gpt-4"
    ai_prompt_template: Optional[str] = None
    ai_parameters: Optional[Dict[str, Any]] = None
    message_template: str
    auto_escalate_after_hours: Optional[int] = None
    escalate_to_role: Optional[str] = None
    apply_to_projects: Optional[List[int]] = None
    apply_to_task_priorities: Optional[List[str]] = None
    apply_to_users: Optional[List[int]] = None
    exclude_users: Optional[List[int]] = None
    is_active: bool = True
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TPMAIAgentConversationSchema(BaseModel):
    id: Optional[int] = None
    tpm_ai_agent_rule_id: int
    tpm_project_id: Optional[int] = None
    tpm_task_event_id: int
    user_id: int
    conversation_type: str
    ai_message: str
    ai_reasoning: Optional[str] = None
    ai_model_used: Optional[str] = None
    user_response: Optional[str] = None
    responded_at: Optional[datetime] = None
    response_time_hours: Optional[float] = None
    task_status_update: Optional[str] = None
    delay_reason: Optional[str] = None
    blockers_identified: Optional[Dict[str, Any]] = None
    new_due_date: Optional[datetime] = None
    sentiment_score: Optional[float] = None
    user_mood: Optional[str] = None
    needs_manager_attention: bool = False
    requires_follow_up: bool = False
    follow_up_at: Optional[datetime] = None
    follow_up_reason: Optional[str] = None
    escalate_to_manager: bool = False
    escalated_at: Optional[datetime] = None
    escalated_to_user_id: Optional[int] = None
    escalation_reason: Optional[str] = None
    conversation_status: str = "sent"
    notification_sent: bool = False
    notification_channel: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
