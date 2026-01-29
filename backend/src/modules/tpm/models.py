from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, UniqueConstraint, Numeric, Index, Date
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from datetime import datetime
from src.infrastructure.database import Base

class TPMTaskStatus(Base):
    __tablename__ = "tpm_master_task_statuses"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    color_code = Column(String(20))
    display_sequence = Column(Integer)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TPMProjectStatus(Base):
    __tablename__ = "tpm_master_project_statuses"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    color_code = Column(String(20))
    display_sequence = Column(Integer)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TPMTag(Base):
    __tablename__ = "tpm_master_task_project_tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    color_code = Column(String(20))
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TPMTaskTemplate(Base):
    __tablename__ = "tpm_master_task_templates"
    id = Column(Integer, primary_key=True)
    title = Column(String(1024), nullable=False)
    task_or_event = Column(Boolean, nullable=False)
    content = Column(Text)
    tags = Column(String(500))
    shared_or_private_template = Column(Boolean, nullable=False)
    published_or_draft = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TPMProject(Base):
    __tablename__ = "tpm_projects"
    id = Column(Integer, primary_key=True)
    name = Column(String(1024), nullable=False)
    project_code = Column(String(128))
    tpm_master_project_status_id = Column(Integer, ForeignKey("tpm_master_project_statuses.id"))
    task_project_tags = Column(JSONB)
    start_date = Column(Date)
    end_date = Column(Date)
    actual_start_date = Column(Date)
    actual_end_date = Column(Date)
    number_of_hours = Column(Integer)
    number_of_working_days = Column(Integer)
    number_of_team_members = Column(Integer)
    number_of_milestones_tasks = Column(Integer)
    milestones_status = Column(Integer)
    progress_percentage = Column(Integer, default=0)
    timeline_status = Column(String(50))
    brief = Column(Text)
    detailed_description = Column(Text)
    estimated_budget = Column(Numeric(12, 2))
    actual_budget = Column(Numeric(12, 2))
    master_currency_id = Column(Integer)
    project_manager_user_id = Column(Integer, ForeignKey("app_users.id"))
    project_owner_user_id = Column(Integer, ForeignKey("app_users.id"))
    is_active = Column(Boolean, default=True)
    is_archived = Column(Boolean, default=False)
    archived_at = Column(DateTime)
    master_hub_id = Column(Integer)
    company_id = Column(Integer)
    institute_id = Column(Integer)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index('idx_projects_status', 'tpm_master_project_status_id'),
        Index('idx_projects_manager', 'project_manager_user_id'),
        Index('idx_projects_dates', 'start_date', 'end_date'),
        Index('idx_projects_active', 'is_active', 'is_archived'),
    )

class TPMProjectDocument(Base):
    __tablename__ = "tpm_project_documents"
    id = Column(Integer, primary_key=True)
    tpm_project_id = Column(Integer, ForeignKey("tpm_projects.id", ondelete="CASCADE"), nullable=False)
    document_type = Column(String(128))
    name = Column(String(1024), nullable=False)
    file_url = Column(String(2048))
    file_size = Column(Integer)
    file_type = Column(String(128))
    uploaded_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index('idx_project_documents_project', 'tpm_project_id'),
        Index('idx_project_documents_type', 'document_type'),
    )

class TPMProjectTeam(Base):
    __tablename__ = "tpm_project_team"
    id = Column(Integer, primary_key=True)
    tpm_project_id = Column(Integer, ForeignKey("tpm_projects.id", ondelete="CASCADE"), nullable=False)
    app_user_id = Column(Integer, ForeignKey("app_users.id"))
    crm_contact_id = Column(Integer)
    full_name = Column(String(256))
    job_title = Column(String(128))
    email = Column(String(256))
    phone = Column(String(50))
    role = Column(String(128))
    responsibilities = Column(Text)
    allocation_percentage = Column(Integer)
    daily_work_hours = Column(Numeric(5, 2))
    is_active = Column(Boolean, default=True)
    joined_date = Column(Date)
    left_date = Column(Date)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index('idx_project_team_project', 'tpm_project_id'),
        Index('idx_project_team_user', 'app_user_id'),
        Index('idx_project_team_active', 'is_active', 'tpm_project_id'),
    )

class TPMProjectNote(Base):
    __tablename__ = "tpm_project_notes"
    id = Column(Integer, primary_key=True)
    tpm_project_id = Column(Integer, ForeignKey("tpm_projects.id", ondelete="CASCADE"), nullable=False)
    parent_note_id = Column(Integer, ForeignKey("tpm_project_notes.id", ondelete="CASCADE"))
    notes = Column(Text)
    note_type = Column(String(50), default='general')
    has_attachments = Column(Boolean, default=False)
    attachments = Column(JSONB)
    linked_document_ids = Column(ARRAY(Integer))
    is_pinned = Column(Boolean, default=False)
    pinned_at = Column(DateTime)
    pinned_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    reply_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    reactions = Column(JSONB)
    is_edited = Column(Boolean, default=False)
    edited_at = Column(DateTime)
    edit_history = Column(JSONB)
    mentioned_user_ids = Column(ARRAY(Integer))
    notification_sent = Column(Boolean, default=False)
    read_by_user_ids = Column(ARRAY(Integer))
    is_important = Column(Boolean, default=False)
    priority = Column(String(20))
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime)
    deleted_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index('idx_project_notes_project', 'tpm_project_id'),
        Index('idx_project_notes_type', 'note_type'),
        Index('idx_project_notes_parent', 'parent_note_id'),
        Index('idx_project_notes_pinned', 'tpm_project_id', 'is_pinned'),
        Index('idx_project_notes_deleted', 'is_deleted', 'tpm_project_id'),
        Index('idx_project_notes_important', 'tpm_project_id', 'is_important'),
    )

class TPMTaskEvent(Base):
    __tablename__ = "tpm_task_events"
    id = Column(Integer, primary_key=True)
    tpm_project_id = Column(Integer, ForeignKey("tpm_projects.id", ondelete="SET NULL"))
    task_or_event = Column(Boolean, nullable=False)
    name = Column(String(2048), nullable=False)
    description = Column(Text)
    tpm_master_task_status_id = Column(Integer, ForeignKey("tpm_master_task_statuses.id"))
    priority = Column(String(50))
    progress = Column(Integer, default=0)
    start_date_time = Column(DateTime)
    end_date_time = Column(DateTime)
    estimated_time_in_hours = Column(Numeric(10, 2))
    actual_time_in_hours = Column(Numeric(10, 2))
    assigned_to_user_id = Column(Integer, ForeignKey("app_users.id"))
    assigned_to_employee_id = Column(Integer)
    save_as_template = Column(Boolean, default=False)
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(String(128))
    tags = Column(ARRAY(String))
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime)
    deleted_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index('idx_task_events_project', 'tpm_project_id'),
        Index('idx_task_events_status', 'tpm_master_task_status_id'),
        Index('idx_task_events_assigned', 'assigned_to_user_id'),
        Index('idx_task_events_dates', 'start_date_time', 'end_date_time'),
        Index('idx_task_events_priority', 'priority'),
    )

class TPMTaskDocument(Base):
    __tablename__ = "tpm_task_documents"
    id = Column(Integer, primary_key=True)
    tpm_task_event_id = Column(Integer, ForeignKey("tpm_task_events.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(1024), nullable=False)
    file_url = Column(String(2048))
    file_size = Column(Integer)
    file_type = Column(String(128))
    uploaded_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index('idx_task_documents_task', 'tpm_task_event_id'),
    )

class TPMTaskTeam(Base):
    __tablename__ = "tpm_task_team"
    id = Column(Integer, primary_key=True)
    tpm_task_event_id = Column(Integer, ForeignKey("tpm_task_events.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("app_users.id"))
    employee_id = Column(Integer)
    contact_id = Column(Integer)
    student_id = Column(Integer)
    tutor_id = Column(Integer)
    name = Column(String(256), nullable=False)
    email = Column(String(256))
    phone = Column(String(50))
    role = Column(String(128))
    invite_accepted = Column(Boolean, default=False)
    attendance_status = Column(String(50))
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index('idx_task_team_task', 'tpm_task_event_id'),
        Index('idx_task_team_user', 'user_id'),
    )

class TPMTaskNote(Base):
    __tablename__ = "tpm_task_notes"
    id = Column(Integer, primary_key=True)
    tpm_task_event_id = Column(Integer, ForeignKey("tpm_task_events.id", ondelete="CASCADE"), nullable=False)
    notes = Column(Text)
    note_type = Column(String(50))
    is_pinned = Column(Boolean, default=False)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index('idx_task_notes_task', 'tpm_task_event_id'),
    )

class TPMTaskWorkItem(Base):
    __tablename__ = "tpm_task_work_items"
    id = Column(Integer, primary_key=True)
    tpm_task_event_id = Column(Integer, ForeignKey("tpm_task_events.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(1024), nullable=False)
    description = Column(Text)
    estimated_hours = Column(Numeric(10, 2))
    actual_hours = Column(Numeric(10, 2))
    start_date_time = Column(DateTime)
    end_date_time = Column(DateTime)
    open_or_closed = Column(Boolean, default=True)
    completed_at = Column(DateTime)
    assigned_to_user_id = Column(Integer, ForeignKey("app_users.id"))
    assign_dated_time = Column(DateTime)
    assigned_to_contact_id = Column(Integer)
    display_sequence = Column(Integer)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index('idx_work_items_task', 'tpm_task_event_id'),
        Index('idx_work_items_assigned', 'assigned_to_user_id'),
        Index('idx_work_items_status', 'open_or_closed'),
    )

class TPMAIAgentRule(Base):
    __tablename__ = "tpm_ai_agent_rules"
    id = Column(Integer, primary_key=True)
    rule_name = Column(String(256), nullable=False)
    description = Column(Text)
    trigger_type = Column(String(50), nullable=False)
    days_before_due = Column(Integer)
    hours_after_overdue = Column(Integer)
    days_without_update = Column(Integer)
    ai_model = Column(String(128), default='gpt-4')
    ai_prompt_template = Column(Text)
    ai_parameters = Column(JSONB)
    message_template = Column(Text, nullable=False)
    auto_escalate_after_hours = Column(Integer)
    escalate_to_role = Column(String(50))
    apply_to_projects = Column(ARRAY(Integer))
    apply_to_task_priorities = Column(ARRAY(String))
    apply_to_users = Column(ARRAY(Integer))
    exclude_users = Column(ARRAY(Integer))
    is_active = Column(Boolean, default=True)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index('idx_agent_rules_active', 'is_active'),
        Index('idx_agent_rules_trigger', 'trigger_type'),
    )

class TPMAIAgentConversation(Base):
    __tablename__ = "tpm_ai_agent_conversations"
    id = Column(Integer, primary_key=True)
    tpm_ai_agent_rule_id = Column(Integer, ForeignKey("tpm_ai_agent_rules.id", ondelete="CASCADE"), nullable=False)
    tpm_project_id = Column(Integer, ForeignKey("tpm_projects.id", ondelete="CASCADE"))
    tpm_task_event_id = Column(Integer, ForeignKey("tpm_task_events.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("app_users.id"), nullable=False)
    conversation_type = Column(String(50), nullable=False)
    ai_message = Column(Text, nullable=False)
    ai_reasoning = Column(Text)
    ai_model_used = Column(String(128))
    user_response = Column(Text)
    responded_at = Column(DateTime)
    response_time_hours = Column(Numeric(10, 2))
    task_status_update = Column(String(128))
    delay_reason = Column(Text)
    blockers_identified = Column(JSONB)
    new_due_date = Column(DateTime)
    sentiment_score = Column(Numeric(5, 2))
    user_mood = Column(String(50))
    needs_manager_attention = Column(Boolean, default=False)
    requires_follow_up = Column(Boolean, default=False)
    follow_up_at = Column(DateTime)
    follow_up_reason = Column(Text)
    escalate_to_manager = Column(Boolean, default=False)
    escalated_at = Column(DateTime)
    escalated_to_user_id = Column(Integer, ForeignKey("app_users.id"))
    escalation_reason = Column(Text)
    conversation_status = Column(String(50), default='sent')
    notification_sent = Column(Boolean, default=False)
    notification_channel = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index('idx_conversations_rule', 'tpm_ai_agent_rule_id'),
        Index('idx_conversations_task', 'tpm_task_event_id'),
        Index('idx_conversations_user', 'user_id'),
        Index('idx_conversations_status', 'conversation_status'),
        Index('idx_conversations_sentiment', 'sentiment_score'),
    )
