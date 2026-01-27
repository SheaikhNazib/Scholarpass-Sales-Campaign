from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date

class CRMCompanySchema(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=512)
    trade_name: Optional[str] = None
    brief_profile: Optional[str] = None
    full_profile: Optional[str] = None
    custom_number: Optional[str] = None
    year_of_establishment: Optional[int] = None
    industry: Optional[str] = None
    market_cap: Optional[float] = None
    number_of_employees: Optional[int] = None
    annual_revenue: Optional[float] = None
    full_address: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    ein_tax_id: Optional[str] = None
    logo_url: Optional[str] = None
    facebook_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None
    is_verified: bool = False
    verified_at: Optional[datetime] = None
    is_active_or_archived: bool = True
    internal_ranking_score: Optional[int] = None
    internal_remarks: Optional[str] = None
    company_snapshot_json: Optional[Dict[str, Any]] = None
    company_snapshot_json_url: Optional[str] = None
    snapshot_generated_at: Optional[datetime] = None
    company_profile_completion: Optional[int] = None
    company_tags_completion: Optional[int] = None
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CRMContactSchema(BaseModel):
    id: Optional[int] = None
    first_name: str = Field(..., min_length=1, max_length=128)
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    tax_id_or_ssn: Optional[str] = None
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    years_of_experience: Optional[int] = None
    full_address: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = None
    mobile: Optional[str] = None
    is_sms_subscribed: bool = False
    is_whatsapp_subscribed: bool = False
    personal_email: Optional[EmailStr] = None
    personal_email_verified: bool = False
    personal_email_subscribed: bool = True
    business_email: Optional[EmailStr] = None
    business_email_verified: bool = False
    business_email_subscribed: bool = True
    brief_profile: Optional[str] = None
    full_profile: Optional[str] = None
    public_profile_url: Optional[str] = None
    internal_notes: Optional[str] = None
    facebook_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None
    is_verified: bool = False
    verified_at: Optional[datetime] = None
    is_active_or_archived: bool = True
    contact_ranking_score: Optional[int] = None
    contact_snapshot_json: Optional[Dict[str, Any]] = None
    contact_snapshot_json_url: Optional[str] = None
    snapshot_generated_at: Optional[datetime] = None
    contact_profile_completion: Optional[int] = None
    contact_tags_completion: Optional[int] = None
    company_id: Optional[int] = None
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CRMGroupSchema(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=256)
    description: Optional[str] = None
    group_type: Optional[str] = None
    is_active: bool = True
    member_count: int = 0
    max_members: Optional[int] = None
    is_public: bool = False
    auto_sync: bool = False
    sync_criteria: Optional[Dict[str, Any]] = None
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CRMGroupMemberSchema(BaseModel):
    id: Optional[int] = None
    member_name: str = Field(..., min_length=1, max_length=256)
    member_email: Optional[EmailStr] = None
    member_phone: Optional[str] = None
    can_receive_messages: bool = True
    can_send_messages: bool = False
    is_admin: bool = False
    is_active: bool = True
    joined_at: Optional[datetime] = None
    removed_at: Optional[datetime] = None
    group_id: int
    contact_id: Optional[int] = None
    user_id: Optional[int] = None
    added_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CRMGroupMessageSchema(BaseModel):
    id: Optional[int] = None
    subject: Optional[str] = None
    body: str
    message_type: str = "broadcast"
    status: str = "pending"
    sent_at: Optional[datetime] = None
    scheduled_for: Optional[datetime] = None
    has_attachments: bool = False
    attachments: Optional[Dict[str, Any]] = None
    total_recipients: int = 0
    delivered_count: int = 0
    viewed_count: int = 0
    clicked_count: int = 0
    group_id: int
    from_group_member_id: Optional[int] = None
    template_id: Optional[int] = None
    sent_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CRMCompanyContactMapSchema(BaseModel):
    id: Optional[int] = None
    company_id: int
    contact_full_name: str = Field(..., min_length=1, max_length=256)
    job_title: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_primary_contact: bool = False
    display_sequence: Optional[int] = None
    is_active: bool = True
    contact_id: int
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CRMNoteSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    notes: str
    note_type: str = "general"
    is_pinned: bool = False
    is_private: bool = False
    company_id: Optional[int] = None
    contact_id: Optional[int] = None
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CRMBankInfoSchema(BaseModel):
    id: Optional[int] = None
    bank_name: str = Field(..., min_length=1, max_length=256)
    account_number: Optional[str] = None
    routing_number: Optional[str] = None
    swift_code: Optional[str] = None
    iban: Optional[str] = None
    wire_account_number: Optional[str] = None
    account_type: Optional[str] = None
    account_holder_name: Optional[str] = None
    bank_address: Optional[str] = None
    bank_city: Optional[str] = None
    bank_state: Optional[str] = None
    bank_country: Optional[str] = None
    account_phone: Optional[str] = None
    account_email: Optional[EmailStr] = None
    is_verified: bool = False
    verified_at: Optional[datetime] = None
    is_active: bool = True
    notes: Optional[str] = None
    contact_id: Optional[int] = None
    company_id: Optional[int] = None
    institute_id: Optional[int] = None
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
