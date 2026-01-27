from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ConnectChannelSchema(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=128)
    code: str = Field(..., min_length=1, max_length=50)
    is_active: bool = True
    display_order: int = 0
    icon_class: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ConnectTemplateSchema(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=1024)
    template_type: str = Field(..., pattern="^(email|sms|whatsapp|both)$")
    category: Optional[str] = None
    public_or_private_template: str = "public"
    subject: Optional[str] = None
    body_content: str = Field(..., min_length=1)
    html_content: Optional[str] = None
    tags: Optional[str] = None
    merge_fields: Optional[Dict[str, Any]] = None
    mail_merge_enabled: bool = False
    published: bool = False
    is_system_template: bool = False
    usage_count: int = 0
    last_used_at: Optional[datetime] = None
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ConnectMessageSchema(BaseModel):
    id: Optional[int] = None
    message_type: str = Field(..., pattern="^(email|sms|whatsapp|chat)$")
    direction: str = Field(..., pattern="^(inbound|outbound)$")
    message_category: Optional[str] = None
    sender_user_id: Optional[int] = None
    sender_name: Optional[str] = None
    sender_email: Optional[EmailStr] = None
    to_recipients: Optional[List[Dict[str, Any]]] = None
    cc_recipients: Optional[List[Dict[str, Any]]] = None
    bcc_recipients: Optional[List[Dict[str, Any]]] = None
    subject: Optional[str] = None
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    attachments: Optional[List[Dict[str, Any]]] = None
    has_attachments: bool = False
    template_id: Optional[int] = None
    merge_data: Optional[Dict[str, Any]] = None
    channel_id: Optional[int] = None
    status: str = "draft"
    is_scheduled: bool = False
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    opened_at: Optional[datetime] = None
    clicked_at: Optional[datetime] = None
    bounced_at: Optional[datetime] = None
    is_opened: bool = False
    is_clicked: bool = False
    open_count: int = 0
    click_count: int = 0
    is_ai_generated: bool = False
    ai_prompt: Optional[str] = None
    ai_model_used: Optional[str] = None
    crm_contact_id: Optional[int] = None
    crm_company_id: Optional[int] = None
    lms_student_id: Optional[int] = None
    lms_educator_id: Optional[int] = None
    thread_id: Optional[str] = None
    reply_to_message_id: Optional[int] = None
    internal_notes: Optional[str] = None
    follow_up_required: bool = False
    message_archived: bool = False
    archived_at_date: Optional[datetime] = None
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ConnectCallSchema(BaseModel):
    id: Optional[int] = None
    call_sid: str = Field(..., min_length=1, max_length=128)
    call_reference: Optional[str] = None
    direction: str = Field(..., pattern="^(inbound|outbound)$")
    from_number: str = Field(..., min_length=1, max_length=50)
    to_number: str = Field(..., min_length=1, max_length=50)
    caller_name: Optional[str] = None
    status: str = Field(..., pattern="^(initiated|ringing|answered|completed|failed|busy|no-answer|canceled)$")
    initiated_at: Optional[datetime] = None
    ringing_at: Optional[datetime] = None
    answered_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    call_purpose: Optional[str] = None
    call_notes: Optional[str] = None
    call_summary: Optional[str] = None
    transcription_text: Optional[str] = None
    recording_url: Optional[str] = None
    recording_duration: Optional[int] = None
    has_recording: bool = False
    is_ai_agent_call: bool = False
    ai_agent_name: Optional[str] = None
    ai_sentiment_score: Optional[float] = None
    ai_call_quality: Optional[str] = None
    call_cost: Optional[float] = None
    currency_code: str = "USD"
    user_id: Optional[int] = None
    contact_id: Optional[int] = None
    student_id: Optional[int] = None
    tutor_id: Optional[int] = None
    company_id: Optional[int] = None
    related_ticket_id: Optional[int] = None
    follow_up_required: bool = False
    follow_up_date: Optional[datetime] = None
    follow_up_notes: Optional[str] = None
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
