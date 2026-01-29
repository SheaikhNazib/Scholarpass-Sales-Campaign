from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, UniqueConstraint, Numeric, Index
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from src.infrastructure.database import Base

class ConnectChannel(Base):
    __tablename__ = "app_connect_channels"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    code = Column(String(50), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    icon_class = Column(String(128))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ConnectTemplate(Base):
    __tablename__ = "app_connect_email_sms_templates"
    id = Column(Integer, primary_key=True)
    title = Column(String(1024), nullable=False)
    template_type = Column(String(50), nullable=False)
    category = Column(String(128))
    public_or_private_template = Column(String(50), default='public')
    subject = Column(String(1024))
    body_content = Column(Text, nullable=False)
    html_content = Column(Text)
    tags = Column(String(500))
    merge_fields = Column(JSONB)
    mail_merge_enabled = Column(Boolean, default=False)
    published = Column(Boolean, default=False)
    is_system_template = Column(Boolean, default=False)
    usage_count = Column(Integer, default=0)
    last_used_at = Column(DateTime)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index('idx_connect_templates_type', 'template_type'),
        Index('idx_connect_templates_category', 'category'),
        Index('idx_connect_templates_published', 'published'),
        Index('idx_connect_templates_creator', 'created_by_user_id'),
    )

class ConnectMessage(Base):
    __tablename__ = "app_connect_contact_messages"
    id = Column(Integer, primary_key=True)
    message_type = Column(String(50), nullable=False)
    direction = Column(String(20), nullable=False)
    message_category = Column(String(128))
    sender_user_id = Column(Integer, ForeignKey("app_users.id"))
    sender_name = Column(String(256))
    sender_email = Column(String(256))
    to_recipients = Column(JSONB)
    cc_recipients = Column(JSONB)
    bcc_recipients = Column(JSONB)
    subject = Column(String(1024))
    body_text = Column(Text)
    body_html = Column(Text)
    attachments = Column(JSONB)
    has_attachments = Column(Boolean, default=False)
    template_id = Column(Integer, ForeignKey("app_connect_email_sms_templates.id"))
    merge_data = Column(JSONB)
    channel_id = Column(Integer, ForeignKey("app_connect_channels.id"))
    status = Column(String(50), default='draft')
    is_scheduled = Column(Boolean, default=False)
    scheduled_at = Column(DateTime)
    sent_at = Column(DateTime)
    delivered_at = Column(DateTime)
    opened_at = Column(DateTime)
    clicked_at = Column(DateTime)
    bounced_at = Column(DateTime)
    is_opened = Column(Boolean, default=False)
    is_clicked = Column(Boolean, default=False)
    open_count = Column(Integer, default=0)
    click_count = Column(Integer, default=0)
    is_ai_generated = Column(Boolean, default=False)
    ai_prompt = Column(Text)
    ai_model_used = Column(String(128))
    crm_contact_id = Column(Integer)
    crm_company_id = Column(Integer)
    lms_student_id = Column(Integer)
    lms_educator_id = Column(Integer)
    thread_id = Column(String(128))
    reply_to_message_id = Column(Integer, ForeignKey("app_connect_contact_messages.id"))
    internal_notes = Column(Text)
    follow_up_required = Column(Boolean, default=False)
    message_archived = Column(Boolean, default=False)
    archived_at_date = Column(DateTime)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index('idx_contact_messages_type', 'message_type', 'direction'),
        Index('idx_contact_messages_status', 'status'),
        Index('idx_contact_messages_scheduled', 'is_scheduled', 'scheduled_at'),
        Index('idx_contact_messages_sent', 'sent_at'),
        Index('idx_contact_messages_contact', 'crm_contact_id'),
        Index('idx_contact_messages_company', 'crm_company_id'),
        Index('idx_contact_messages_thread', 'thread_id'),
        Index('idx_contact_messages_channel', 'channel_id'),
    )

class ConnectCall(Base):
    __tablename__ = "app_connect_calls"
    id = Column(Integer, primary_key=True)
    call_sid = Column(String(128), nullable=False, unique=True)
    call_reference = Column(String(128))
    direction = Column(String(20), nullable=False)
    from_number = Column(String(50), nullable=False)
    to_number = Column(String(50), nullable=False)
    caller_name = Column(String(256))
    status = Column(String(50), nullable=False)
    initiated_at = Column(DateTime, default=datetime.utcnow)
    ringing_at = Column(DateTime)
    answered_at = Column(DateTime)
    ended_at = Column(DateTime)
    duration_seconds = Column(Integer)
    call_purpose = Column(String(256))
    call_notes = Column(Text)
    call_summary = Column(Text)
    transcription_text = Column(Text)
    recording_url = Column(String(2048))
    recording_duration = Column(Integer)
    has_recording = Column(Boolean, default=False)
    is_ai_agent_call = Column(Boolean, default=False)
    ai_agent_name = Column(String(128))
    ai_sentiment_score = Column(Numeric(3, 2))
    ai_call_quality = Column(String(50))
    call_cost = Column(Numeric(10, 4))
    currency_code = Column(String(10), default='USD')
    user_id = Column(Integer, ForeignKey("app_users.id"))
    contact_id = Column(Integer)
    student_id = Column(Integer)
    tutor_id = Column(Integer)
    company_id = Column(Integer)
    related_ticket_id = Column(Integer)
    follow_up_required = Column(Boolean, default=False)
    follow_up_date = Column(DateTime)
    follow_up_notes = Column(Text)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index('idx_connect_calls_sid', 'call_sid'),
        Index('idx_connect_calls_status', 'status', 'direction'),
        Index('idx_connect_calls_dates', 'initiated_at', 'answered_at'),
        Index('idx_connect_calls_user', 'user_id'),
        Index('idx_connect_calls_contact', 'contact_id'),
        Index('idx_connect_calls_student', 'student_id'),
        Index('idx_connect_calls_from', 'from_number'),
        Index('idx_connect_calls_to', 'to_number'),
        Index('idx_connect_calls_follow_up', 'follow_up_required', 'follow_up_date'),
    )
