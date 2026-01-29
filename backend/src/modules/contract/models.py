from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, UniqueConstraint, Numeric, Index, Date, LargeBinary
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from src.infrastructure.database import Base

class CRMContractType(Base):
    __tablename__ = "crm_master_contract_types"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    description = Column(Text)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMContractCommissionType(Base):
    __tablename__ = "crm_master_contract_commission_types"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    percentage = Column(Numeric(5, 2))
    fixed_amount = Column(Numeric(10, 2))
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CRMContract(Base):
    __tablename__ = "crm_contracts"
    id = Column(Integer, primary_key=True)
    crm_master_contract_type_id = Column(Integer, ForeignKey("crm_master_contract_types.id"))
    crm_master_contract_commission_type_id = Column(Integer, ForeignKey("crm_master_contract_commission_types.id"))
    title = Column(String(1024), nullable=False)
    contract_reference_number = Column(String(256))
    name_of_party_a = Column(String(256))
    name_of_party_b = Column(String(256))
    start_date = Column(Date)
    end_date = Column(Date)
    signed_date = Column(DateTime)
    description = Column(Text)
    remarks = Column(Text)
    signed_and_completed = Column(Boolean, default=False)
    active_or_expired = Column(Boolean, default=True)
    auto_renew = Column(Boolean, default=False)
    contract_value = Column(Numeric(12, 2))
    currency_code = Column(String(10), default='USD')
    pdf_file_url = Column(String(1024))
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime)
    __table_args__ = (
        Index('idx_crm_contracts_type', 'crm_master_contract_type_id'),
        Index('idx_crm_contracts_status', 'active_or_expired', 'signed_and_completed'),
        Index('idx_crm_contracts_dates', 'start_date', 'end_date'),
        Index('idx_crm_contracts_reference', 'contract_reference_number'),
    )

class CRMContractTerm(Base):
    __tablename__ = "crm_contract_terms"
    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey("crm_contracts.id", ondelete="CASCADE"), nullable=False)
    term_name = Column(String(1024))
    terms_type = Column(String(50))
    description = Column(Text)
    seller_percentage = Column(Numeric(5, 2))
    platform_percentage = Column(Numeric(5, 2))
    territory_partner_percentage = Column(Numeric(5, 2))
    marketer_percentage = Column(Numeric(5, 2))
    platform_transaction_fee_amount = Column(Numeric(10, 2))
    lms_course_id = Column(Integer)
    shop_product_id = Column(Integer)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index('idx_contract_terms_contract', 'contract_id'),
        Index('idx_contract_terms_type', 'terms_type'),
        Index('idx_contract_terms_course', 'lms_course_id'),
        Index('idx_contract_terms_product', 'shop_product_id'),
    )

class CRMContractMultiplePartiesSign(Base):
    __tablename__ = "crm_contract_multiple_parties_signs"
    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey("crm_contracts.id", ondelete="CASCADE"), nullable=False)
    party_referred_as = Column(String(256))
    full_name = Column(String(256), nullable=False)
    company_name = Column(String(256))
    job_title = Column(String(128))
    full_address = Column(String(2024))
    phone = Column(String(50))
    email_address = Column(String(256))
    signed = Column(Boolean, default=False)
    sign_date_time = Column(DateTime)
    signature_method = Column(String(50))
    ip_address = Column(String(128))
    mac_address = Column(String(128))
    device_info = Column(Text)
    geolocation = Column(String(256))
    signature_image_url = Column(String(1024))
    signature_binary = Column(LargeBinary)
    user_id = Column(Integer, ForeignKey("app_users.id"))
    crm_contact_id = Column(Integer, ForeignKey("crm_contacts.id"))
    crm_company_id = Column(Integer, ForeignKey("crm_companies.id"))
    lms_educator_id = Column(Integer)
    lms_institute_id = Column(Integer)
    lms_student_id = Column(Integer)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index('idx_contract_signs_contract', 'contract_id'),
        Index('idx_contract_signs_status', 'signed', 'sign_date_time'),
        Index('idx_contract_signs_user', 'user_id'),
        Index('idx_contract_signs_email', 'email_address'),
    )

class CRMContractTrackerTaskReminder(Base):
    __tablename__ = "crm_contract_tracker_task_reminders"
    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey("crm_contracts.id", ondelete="CASCADE"), nullable=False)
    task_event_id = Column(Integer)
    title = Column(String(512), nullable=False)
    description = Column(Text)
    reminder_type = Column(String(50))
    due_date = Column(DateTime, nullable=False)
    reminder_days_before = Column(Integer)
    completed = Column(Boolean, default=False)
    completed_date = Column(DateTime)
    assigned_to_user_id = Column(Integer, ForeignKey("app_users.id"))
    assign_all_parties = Column(JSONB)
    send_email = Column(Boolean, default=True)
    send_sms = Column(Boolean, default=False)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    updated_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index('idx_contract_reminders_contract', 'contract_id'),
        Index('idx_contract_reminders_due_date', 'due_date'),
        Index('idx_contract_reminders_status', 'completed', 'due_date'),
        Index('idx_contract_reminders_assigned', 'assigned_to_user_id'),
    )
