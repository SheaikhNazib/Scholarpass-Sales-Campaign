from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, UniqueConstraint, Numeric, Index
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from src.infrastructure.database import Base

class AppUser(Base):
    __tablename__ = "app_users"
    id = Column(Integer, primary_key=True)
    username = Column(String(256), unique=True, nullable=False)
    password_hash = Column(String(1024), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128))
    email = Column(String(256), unique=True, nullable=False)
    phone_number = Column(String(50))
    master_hub_id = Column(Integer)
    master_country_id = Column(Integer)
    country_phone_id = Column(Integer)
    active_or_archive = Column(Boolean, default=True)
    email_confirmed = Column(Boolean, default=False)
    account_lock = Column(Boolean, default=False)
    phone_number_confirmed = Column(Boolean, default=False)
    two_factor_enabled = Column(Boolean, default=False)
    lockout_enabled = Column(Boolean, default=False)
    access_failed_count = Column(Integer, default=0)
    lockout_end = Column(DateTime)
    profile_picture_url = Column(String(1024))
    whatsapp_subscribed = Column(Boolean, default=False)
    email_subscribed = Column(Boolean, default=False)
    sms_subscribed = Column(Boolean, default=False)
    is_public_user_internal = Column(Boolean, default=False)
    address = Column(String(1024))
    city = Column(String(256))
    state = Column(String(256))
    zip_code = Column(String(50))
    user_profile_tags_json = Column(JSONB)
    user_profile_tags_url = Column(String(1024))
    json_file_updated_at = Column(DateTime)
    primary_role_id = Column(Integer, ForeignKey("app_access_master_roles.id"))
    primary_learning_hub_id = Column(Integer)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AppRole(Base):
    __tablename__ = "app_access_master_roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    display_sequence = Column(Integer)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserRole(Base):
    __tablename__ = "app_access_user_multiple_roles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("app_users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("app_access_master_roles.id", ondelete="CASCADE"), nullable=False)
    assigned_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    assigned_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (UniqueConstraint("user_id", "role_id", name="uq_user_role"),)

class UserOTP(Base):
    __tablename__ = "app_access_user_otps"
    id = Column(Integer, primary_key=True)
    otp = Column(String(6), nullable=False)
    otp_type = Column(String(50), default="email")
    purpose = Column(String(50))
    expiry_time = Column(DateTime, nullable=False)
    is_verified = Column(Boolean, default=False)
    verified_at = Column(DateTime)
    resend_attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=3)
    user_id = Column(Integer, ForeignKey("app_users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserSession(Base):
    __tablename__ = "app_access_user_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("app_users.id", ondelete="CASCADE"), nullable=False)
    session_token = Column(String(512), unique=True, nullable=False)
    device_type = Column(String(50))
    device_os = Column(String(50))
    device_browser = Column(String(100))
    device_ip = Column(String(50))
    login_at = Column(DateTime, default=datetime.utcnow)
    logout_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserNotification(Base):
    __tablename__ = "app_user_notifications"
    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    message = Column(Text)
    notification_type = Column(String(50))
    priority = Column(String(20), default="normal")
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime)
    action_url = Column(String(1024))
    action_label = Column(String(128))
    user_id = Column(Integer, ForeignKey("app_users.id", ondelete="CASCADE"), nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("app_users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
