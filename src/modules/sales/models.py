from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, UniqueConstraint, Numeric, Index, Date, BigInteger
from sqlalchemy.dialects.postgresql import JSONB, ARRAY, DOUBLE_PRECISION
from datetime import datetime
from src.infrastructure.database import Base

class CRMSalesLeadSourceChannel(Base):
    __tablename__ = "crm_sales_lead_source_channels"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    lead_source_link = Column(String(1024))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMSalesLeadStatus(Base):
    __tablename__ = "crm_sales_lead_statuses"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    sequence_number = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMProposalStatus(Base):
    __tablename__ = "crm_proposal_statuses"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    color_code = Column(String(64))
    sequence = Column(Integer)
    is_final = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMProposalType(Base):
    __tablename__ = "crm_proposal_types"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMProposalTemplate(Base):
    __tablename__ = "crm_proposal_templates"
    id = Column(Integer, primary_key=True)
    title = Column(String(1024), nullable=False)
    instruction = Column(String(5000))
    proposals = Column(Text)
    csr_or_grants = Column(Boolean, nullable=False)
    tags = Column(String(500))
    published_or_draft = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMSalesCampaign(Base):
    __tablename__ = "crm_sales_campaigns"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(Text)
    location = Column(String(1024))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    duration = Column(String(128))
    projected_revenue = Column(DOUBLE_PRECISION)
    revenue_earned = Column(DOUBLE_PRECISION)
    projected_sales = Column(Integer)
    number_of_sales = Column(Integer)
    campaign_budget = Column(DOUBLE_PRECISION)
    spent_amount = Column(DOUBLE_PRECISION)
    status_open_closed = Column(Boolean)
    deleted_at = Column(DateTime)
    primary_manager_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMSalesCampaignCompany(Base):
    __tablename__ = "crm_sales_campaign_company"
    id = Column(Integer, primary_key=True)
    company_name = Column(String(256))
    city = Column(String(256))
    website = Column(String(2048))
    sales_score = Column(Integer)
    crm_sales_campaign_id = Column(Integer, ForeignKey("crm_sales_campaigns.id"))
    crm_company_id = Column(Integer, ForeignKey("crm_companies.id"))
    active_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMSalesCampaignContact(Base):
    __tablename__ = "crm_sales_campaign_contact"
    id = Column(Integer, primary_key=True)
    contact_name = Column(String(256))
    phone = Column(String(256))
    email = Column(String(256))
    sales_score = Column(Integer)
    active_archived = Column(Boolean, default=False)
    crm_sales_campaign_id = Column(Integer, ForeignKey("crm_sales_campaigns.id"))
    crm_contact_id = Column(Integer, ForeignKey("crm_contacts.id"))
    crm_company_id = Column(Integer, ForeignKey("crm_companies.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMSalesCampaignExecutionTeam(Base):
    __tablename__ = "crm_sales_campaign_execution_team"
    id = Column(Integer, primary_key=True)
    is_primary = Column(Boolean, nullable=False)
    assigned_date = Column(DateTime)
    notes = Column(Text)
    crm_sales_campaign_id = Column(Integer, ForeignKey("crm_sales_campaigns.id"))
    user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMSalesCampaignTodo(Base):
    __tablename__ = "crm_sales_campaign_todos"
    id = Column(Integer, primary_key=True)
    title = Column(String(512), nullable=False)
    description = Column(Text)
    due_date = Column(DateTime)
    priority = Column(String(50))
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime)
    crm_sales_campaign_id = Column(Integer, ForeignKey("crm_sales_campaigns.id"), nullable=False)
    assigned_to_user_id = Column(Integer, ForeignKey("app_users.id"))
    completed_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMSalesCampaignDocument(Base):
    __tablename__ = "crm_sales_campaign_documents"
    id = Column(Integer, primary_key=True)
    document_title = Column(String(1024), nullable=False)
    document_type = Column(String(128))
    file_binary_object_id = Column(String(2048), nullable=False)
    description = Column(Text)
    crm_sales_campaign_id = Column(Integer, ForeignKey("crm_sales_campaigns.id"), nullable=False)
    uploaded_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMSalesCampaignNote(Base):
    __tablename__ = "crm_sales_campaign_notes"
    id = Column(Integer, primary_key=True)
    note_title = Column(String(512))
    note_content = Column(Text, nullable=False)
    note_type = Column(String(128))
    crm_sales_campaign_id = Column(Integer, ForeignKey("crm_sales_campaigns.id"), nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMSalesLeadOpportunity(Base):
    __tablename__ = "crm_sales_leads_opportunities"
    id = Column(Integer, primary_key=True)
    title = Column(String(512), nullable=False)
    first_name = Column(String(256))
    last_name = Column(String(256))
    email = Column(String(256))
    phone = Column(String(50))
    job_title = Column(String(512))
    description = Column(Text)
    lead_score = Column(Integer)
    referral_code = Column(String(128))
    referred_by_email = Column(String(256))
    referred_by_phone = Column(String(50))
    lead_generation_link = Column(String(512))
    expected_sales_amount = Column(DOUBLE_PRECISION)
    expected_closing_date = Column(DateTime)
    created_date = Column(DateTime)
    zone_id = Column(Integer)
    crm_sales_campaign_id = Column(Integer, ForeignKey("crm_sales_campaigns.id"))
    crm_contact_id = Column(Integer, ForeignKey("crm_contacts.id"))
    crm_company_id = Column(Integer, ForeignKey("crm_companies.id"))
    shop_product_id = Column(Integer)
    lms_course_id = Column(Integer)
    crm_sales_lead_source_channel_id = Column(Integer, ForeignKey("crm_sales_lead_source_channels.id"))
    crm_sales_lead_status_id = Column(Integer, ForeignKey("crm_sales_lead_statuses.id"))
    lead_owner_user_id = Column(Integer, ForeignKey("app_users.id"))
    currency_id = Column(Integer)
    user_id = Column(Integer, ForeignKey("app_users.id"))
    is_app_user = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMSalesLeadNote(Base):
    __tablename__ = "crm_sales_lead_notes"
    id = Column(Integer, primary_key=True)
    crm_sales_lead_opportunity_id = Column(Integer, ForeignKey("crm_sales_leads_opportunities.id"))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMSalesProjection(Base):
    __tablename__ = "crm_sales_projections"
    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    master_duration_type_id = Column(Integer)
    master_fiscal_quarter_id = Column(Integer)
    expected_sales_amount = Column(DOUBLE_PRECISION)
    actual_sales_amount = Column(DOUBLE_PRECISION)
    expected_units_sold = Column(Integer)
    actual_units_sold = Column(Integer)
    expected_transactions = Column(Integer)
    actual_transactions = Column(Integer)
    master_currency_id = Column(Integer)
    zone_id = Column(Integer)
    store_id = Column(Integer)
    shop_product_id = Column(Integer)
    shop_product_category_id = Column(Integer)
    crm_sales_campaign_id = Column(Integer, ForeignKey("crm_sales_campaigns.id"))
    projection_type = Column(String(50), nullable=False)
    sales_projection_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMSalesTractionReport(Base):
    __tablename__ = "crm_sales_traction_reports"
    id = Column(Integer, primary_key=True)
    report_title = Column(String(512), nullable=False)
    report_period_start = Column(DateTime, nullable=False)
    report_period_end = Column(DateTime, nullable=False)
    report_type = Column(String(128))
    total_expected_sales_amount = Column(DOUBLE_PRECISION)
    total_actual_sales_amount = Column(DOUBLE_PRECISION)
    sales_variance_amount = Column(DOUBLE_PRECISION)
    sales_variance_percent = Column(Numeric(5, 2))
    total_expected_units = Column(Integer)
    total_actual_units = Column(Integer)
    units_variance = Column(Integer)
    total_expected_transactions = Column(Integer)
    total_actual_transactions = Column(Integer)
    average_transaction_value = Column(DOUBLE_PRECISION)
    average_units_per_transaction = Column(Numeric(10, 2))
    master_currency_id = Column(Integer)
    crm_sales_campaign_id = Column(Integer, ForeignKey("crm_sales_campaigns.id"))
    zone_id = Column(Integer)
    shop_product_id = Column(Integer)
    shop_product_category_id = Column(Integer)
    store_id = Column(Integer)
    sales_rep_user_id = Column(Integer, ForeignKey("app_users.id"))
    key_insights = Column(Text)
    performance_summary = Column(Text)
    recommendations = Column(Text)
    generated_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    generated_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMProposal(Base):
    __tablename__ = "crm_proposals"
    id = Column(Integer, primary_key=True)
    title = Column(String(1024), nullable=False)
    short_summary = Column(String(2000))
    full_content = Column(Text)
    amount_requested = Column(Numeric(12, 2))
    master_currency_id = Column(Integer)
    proposal_status_id = Column(Integer, ForeignKey("crm_proposal_statuses.id"))
    proposal_type_id = Column(Integer, ForeignKey("crm_proposal_types.id"))
    proposal_template_id = Column(Integer, ForeignKey("crm_proposal_templates.id"))
    primary_company_id = Column(Integer, ForeignKey("crm_companies.id"))
    primary_contact_id = Column(Integer, ForeignKey("crm_contacts.id"))
    scholarship_id = Column(Integer)
    owner_user_id = Column(Integer, ForeignKey("app_users.id"))
    zone_id = Column(Integer)
    expected_response_date = Column(DateTime)
    submission_deadline = Column(DateTime)
    submitted_at = Column(DateTime)
    won_at = Column(DateTime)
    lost_at = Column(DateTime)
    lost_reason = Column(Text)
    tags = Column(ARRAY(String), default=[])
    ai_generated = Column(Boolean, default=False)
    ai_metadata = Column(JSONB)
    ai_model_id = Column(Integer)
    internal_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMProposalRecipient(Base):
    __tablename__ = "crm_proposal_recipients"
    id = Column(Integer, primary_key=True)
    proposal_id = Column(Integer, ForeignKey("crm_proposals.id", ondelete="CASCADE"), nullable=False)
    company_id = Column(Integer, ForeignKey("crm_companies.id"))
    contact_id = Column(Integer, ForeignKey("crm_contacts.id"))
    recipient_role = Column(String(50))
    channel_preference = Column(String(50))
    custom_email = Column(String(256))
    custom_website_url = Column(String(2048))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMProposalSubmission(Base):
    __tablename__ = "crm_proposal_submissions"
    id = Column(Integer, primary_key=True)
    proposal_id = Column(Integer, ForeignKey("crm_proposals.id", ondelete="CASCADE"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("crm_proposal_recipients.id"))
    connect_message_id = Column(Integer)
    channel_type = Column(String(50), nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default='submitted')
    external_reference = Column(String(512))
    response_status = Column(String(128))
    response_date = Column(DateTime)
    response_notes = Column(Text)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMProposalDocument(Base):
    __tablename__ = "crm_proposal_documents"
    id = Column(Integer, primary_key=True)
    proposal_id = Column(Integer, ForeignKey("crm_proposals.id", ondelete="CASCADE"), nullable=False)
    document_title = Column(String(1024), nullable=False)
    file_binary_object_id = Column(String(2048), nullable=False)
    is_primary_version = Column(Boolean, default=False)
    version_number = Column(Integer)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMCompanyProfileAICache(Base):
    __tablename__ = "crm_company_profiles_ai_cache"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("crm_companies.id"), nullable=False, unique=True)
    ai_context_text = Column(Text, nullable=False)
    ai_metadata = Column(JSONB)
    updated_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
