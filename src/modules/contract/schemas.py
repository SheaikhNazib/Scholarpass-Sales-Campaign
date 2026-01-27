from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date

class CRMContractSchema(BaseModel):
    id: Optional[int] = None
    crm_master_contract_type_id: Optional[int] = None
    crm_master_contract_commission_type_id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=1024)
    contract_reference_number: Optional[str] = None
    name_of_party_a: Optional[str] = None
    name_of_party_b: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    signed_date: Optional[datetime] = None
    description: Optional[str] = None
    remarks: Optional[str] = None
    signed_and_completed: bool = False
    active_or_expired: bool = True
    auto_renew: bool = False
    contract_value: Optional[float] = None
    currency_code: str = "USD"
    pdf_file_url: Optional[str] = None
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CRMContractTermSchema(BaseModel):
    id: Optional[int] = None
    contract_id: int
    term_name: Optional[str] = None
    terms_type: Optional[str] = None
    description: Optional[str] = None
    seller_percentage: Optional[float] = None
    platform_percentage: Optional[float] = None
    territory_partner_percentage: Optional[float] = None
    marketer_percentage: Optional[float] = None
    platform_transaction_fee_amount: Optional[float] = None
    lms_course_id: Optional[int] = None
    shop_product_id: Optional[int] = None
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CRMContractMultiplePartiesSignSchema(BaseModel):
    id: Optional[int] = None
    contract_id: int
    party_referred_as: Optional[str] = None
    full_name: str = Field(..., min_length=1, max_length=256)
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    full_address: Optional[str] = None
    phone: Optional[str] = None
    email_address: Optional[EmailStr] = None
    signed: bool = False
    sign_date_time: Optional[datetime] = None
    signature_method: Optional[str] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    device_info: Optional[str] = None
    geolocation: Optional[str] = None
    signature_image_url: Optional[str] = None
    user_id: Optional[int] = None
    crm_contact_id: Optional[int] = None
    crm_company_id: Optional[int] = None
    lms_educator_id: Optional[int] = None
    lms_institute_id: Optional[int] = None
    lms_student_id: Optional[int] = None
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CRMContractTrackerTaskReminderSchema(BaseModel):
    id: Optional[int] = None
    contract_id: int
    task_event_id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=512)
    description: Optional[str] = None
    reminder_type: Optional[str] = None
    due_date: datetime
    reminder_days_before: Optional[int] = None
    completed: bool = False
    completed_date: Optional[datetime] = None
    assigned_to_user_id: Optional[int] = None
    assign_all_parties: Optional[Dict[str, Any]] = None
    send_email: bool = True
    send_sms: bool = False
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
