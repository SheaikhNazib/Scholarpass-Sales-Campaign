from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class CRMSalesCampaignSchema(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=128)
    description: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    duration: Optional[str] = None
    projected_revenue: Optional[float] = None
    revenue_earned: Optional[float] = None
    projected_sales: Optional[int] = None
    number_of_sales: Optional[int] = None
    campaign_budget: Optional[float] = None
    spent_amount: Optional[float] = None
    status_open_closed: Optional[bool] = None
    deleted_at: Optional[datetime] = None
    primary_manager_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CRMSalesLeadOpportunitySchema(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=512)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    job_title: Optional[str] = None
    description: Optional[str] = None
    lead_score: Optional[int] = None
    referral_code: Optional[str] = None
    referred_by_email: Optional[EmailStr] = None
    referred_by_phone: Optional[str] = None
    lead_generation_link: Optional[str] = None
    expected_sales_amount: Optional[float] = None
    expected_closing_date: Optional[datetime] = None
    created_date: Optional[datetime] = None
    zone_id: Optional[int] = None
    crm_sales_campaign_id: Optional[int] = None
    crm_contact_id: Optional[int] = None
    crm_company_id: Optional[int] = None
    shop_product_id: Optional[int] = None
    lms_course_id: Optional[int] = None
    crm_sales_lead_source_channel_id: Optional[int] = None
    crm_sales_lead_status_id: Optional[int] = None
    lead_owner_user_id: Optional[int] = None
    currency_id: Optional[int] = None
    user_id: Optional[int] = None
    is_app_user: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CRMProposalSchema(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=1024)
    short_summary: Optional[str] = None
    full_content: Optional[str] = None
    amount_requested: Optional[float] = None
    master_currency_id: Optional[int] = None
    proposal_status_id: Optional[int] = None
    proposal_type_id: Optional[int] = None
    proposal_template_id: Optional[int] = None
    primary_company_id: Optional[int] = None
    primary_contact_id: Optional[int] = None
    scholarship_id: Optional[int] = None
    owner_user_id: Optional[int] = None
    zone_id: Optional[int] = None
    expected_response_date: Optional[datetime] = None
    submission_deadline: Optional[datetime] = None
    submitted_at: Optional[datetime] = None
    won_at: Optional[datetime] = None
    lost_at: Optional[datetime] = None
    lost_reason: Optional[str] = None
    tags: Optional[List[str]] = None
    ai_generated: bool = False
    ai_metadata: Optional[Dict[str, Any]] = None
    ai_model_id: Optional[int] = None
    internal_notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CRMProposalRecipientSchema(BaseModel):
    id: Optional[int] = None
    proposal_id: int
    company_id: Optional[int] = None
    contact_id: Optional[int] = None
    recipient_role: Optional[str] = None
    channel_preference: Optional[str] = None
    custom_email: Optional[EmailStr] = None
    custom_website_url: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CRMProposalSubmissionSchema(BaseModel):
    id: Optional[int] = None
    proposal_id: int
    recipient_id: Optional[int] = None
    connect_message_id: Optional[int] = None
    channel_type: str
    submitted_at: Optional[datetime] = None
    status: str = "submitted"
    external_reference: Optional[str] = None
    response_status: Optional[str] = None
    response_date: Optional[datetime] = None
    response_notes: Optional[str] = None
    created_by_user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CRMSalesTractionReportSchema(BaseModel):
    id: Optional[int] = None
    report_title: str = Field(..., min_length=1, max_length=512)
    report_period_start: datetime
    report_period_end: datetime
    report_type: Optional[str] = None
    total_expected_sales_amount: Optional[float] = None
    total_actual_sales_amount: Optional[float] = None
    sales_variance_amount: Optional[float] = None
    sales_variance_percent: Optional[float] = None
    total_expected_units: Optional[int] = None
    total_actual_units: Optional[int] = None
    units_variance: Optional[int] = None
    total_expected_transactions: Optional[int] = None
    total_actual_transactions: Optional[int] = None
    average_transaction_value: Optional[float] = None
    average_units_per_transaction: Optional[float] = None
    master_currency_id: Optional[int] = None
    crm_sales_campaign_id: Optional[int] = None
    zone_id: Optional[int] = None
    shop_product_id: Optional[int] = None
    shop_product_category_id: Optional[int] = None
    store_id: Optional[int] = None
    sales_rep_user_id: Optional[int] = None
    key_insights: Optional[str] = None
    performance_summary: Optional[str] = None
    recommendations: Optional[str] = None
    generated_by_user_id: Optional[int] = None
    generated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
