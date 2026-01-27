from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, UniqueConstraint, Index, Numeric
from datetime import datetime
from src.infrastructure.database import Base

class Country(Base):
    __tablename__ = "master_countries"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    ticker = Column(String(50))
    flag_icon = Column(String(128))
    country_phone_code = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class State(Base):
    __tablename__ = "master_states"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    ticker = Column(String(50))
    master_country_id = Column(Integer, ForeignKey("master_countries.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class County(Base):
    __tablename__ = "master_counties"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    master_country_id = Column(Integer, ForeignKey("master_countries.id"))
    master_state_id = Column(Integer, ForeignKey("master_states.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class City(Base):
    __tablename__ = "master_cities"
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    master_country_id = Column(Integer, ForeignKey("master_countries.id"))
    master_state_id = Column(Integer, ForeignKey("master_states.id"))
    master_county_id = Column(Integer, ForeignKey("master_counties.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ZipCode(Base):
    __tablename__ = "master_zip_codes"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    master_country_id = Column(Integer, ForeignKey("master_countries.id"))
    master_state_id = Column(Integer, ForeignKey("master_states.id"))
    master_county_id = Column(Integer, ForeignKey("master_counties.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Currency(Base):
    __tablename__ = "master_currencies"
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    ticker = Column(String(32))
    icon = Column(String(256))
    master_country_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Language(Base):
    __tablename__ = "master_languages"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TimeZone(Base):
    __tablename__ = "master_time_zones"
    id = Column(Integer, primary_key=True)
    timezone_name = Column(String(128), nullable=False, unique=True)
    utc_offset_minutes = Column(Integer, nullable=False)
    is_default = Column(Boolean, default=False)
    master_country_id = Column(Integer)
    master_city_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HubType(Base):
    __tablename__ = "master_hub_types"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Hub(Base):
    __tablename__ = "master_hubs"
    id = Column(Integer, primary_key=True)
    master_hub_type_id = Column(Integer, ForeignKey("master_hub_types.id"))
    has_parent_hub = Column(Boolean, default=False)
    parent_master_hub_id = Column(Integer, ForeignKey("master_hubs.id"))
    name = Column(String(256))
    description = Column(Text)
    country_name = Column(String(128))
    state_name = Column(String(128))
    city_name = Column(String(128))
    hub_office_address = Column(String(1500))
    latitude = Column(String(20))
    longitude = Column(String(20))
    is_active_or_planning = Column(Boolean, default=False)
    custom_url = Column(String(128))
    manage_by_partner_or_corporate = Column(Boolean, default=False)
    projected_yearly_revenue = Column(String(20))
    display_score_sequence = Column(Integer)
    population_stats = Column(Integer)
    company_stats = Column(Integer)
    contact_stats = Column(Integer)
    institute_stats = Column(Integer)
    job_stats = Column(Integer)
    store_stats = Column(Integer)
    student_stats = Column(Integer)
    master_country_id = Column(Integer, ForeignKey("master_countries.id"))
    master_state_id = Column(Integer, ForeignKey("master_states.id"))
    master_city_id = Column(Integer, ForeignKey("master_cities.id"))
    master_languages_id = Column(Integer, ForeignKey("master_languages.id"))
    master_currency_id = Column(Integer, ForeignKey("master_currencies.id"))
    master_time_zone_id = Column(Integer, ForeignKey("master_time_zones.id"))
    hub_manager_user_id = Column(Integer)
    hub_manager_name = Column(String(256))
    hub_manager_email = Column(String(256))
    hub_manager_phone = Column(String(50))
    created_by_user_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AIModel(Base):
    __tablename__ = "master_ai_models"
    id = Column(Integer, primary_key=True)
    model_name = Column(String(255), nullable=False)
    provider_name = Column(String(255), nullable=False)
    model_version = Column(String(255))
    best_for = Column(Text)
    is_active = Column(Boolean, default=False)
    display_sequence = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (UniqueConstraint("model_name", "model_version", name="uq_ai_model_version"),)

class AIPromptLibrary(Base):
    __tablename__ = "master_ai_prompt_libraries"
    id = Column(Integer, primary_key=True)
    title = Column(String(1024), nullable=False)
    category = Column(String(128))
    prompt_template = Column(Text, nullable=False)
    usage_instructions = Column(Text)
    applicable_entities = Column(String(1024))
    recommended_ai_model_id = Column(Integer, ForeignKey("master_ai_models.id"))
    temperature = Column(String(10), default='0.7')
    max_tokens = Column(Integer, default=2000)
    example_input = Column(Text)
    example_output = Column(Text)
    is_published = Column(Boolean, default=False)
    is_system_template = Column(Boolean, default=False)
    tags = Column(String(512))
    usage_count = Column(Integer, default=0)
    avg_rating = Column(String(10))
    created_by_user_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index("idx_prompt_libraries_category", "category"),
        Index("idx_prompt_libraries_published", "is_published"),
        Index("idx_prompt_libraries_model", "recommended_ai_model_id"),
    )

class DurationType(Base):
    __tablename__ = "master_duration_types"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    number_of_days = Column(Integer)
    display_sequence = Column(Integer, default=0)
    created_by_user_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AppSubscriptionType(Base):
    __tablename__ = "master_app_subscription_types"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    key_features = Column(Text)
    description = Column(Text)
    icon_url = Column(String(1024))
    price = Column(String(20))
    offer_wallet_credit = Column(String(20), default='0')
    master_currency_id = Column(String(10), default='USD')
    master_duration_type_id = Column(Integer, ForeignKey("master_duration_types.id"))
    is_active = Column(Boolean, default=True)
    display_sequence = Column(Integer, default=0)
    created_by_user_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TagGroup(Base):
    __tablename__ = "master_tag_groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(1024))
    description = Column(Text)
    is_public_or_private_tag = Column(Boolean, default=True)
    created_by_user_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TagCategory(Base):
    __tablename__ = "master_tag_categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(1024), nullable=False)
    description = Column(Text)
    is_public_or_private_tag = Column(Boolean, default=True)
    master_tag_group_id = Column(Integer, ForeignKey("master_tag_groups.id"))
    created_by_user_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Tag(Base):
    __tablename__ = "master_tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(Text)
    synonyms = Column(String(5000))
    display_sequence = Column(Integer)
    image_url = Column(String(1024))
    master_tag_group_id = Column(Integer, ForeignKey("master_tag_groups.id"))
    tag_group_name = Column(String(1024))
    tag_category_name = Column(String(1024))
    master_tag_category_id = Column(Integer, ForeignKey("master_tag_categories.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FiscalQuarter(Base):
    __tablename__ = "master_fiscal_quarters"
    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    master_duration_type_id = Column(Integer, ForeignKey("master_duration_types.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
