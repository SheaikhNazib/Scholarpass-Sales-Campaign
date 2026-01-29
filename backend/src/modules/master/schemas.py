from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CountryResponse(BaseModel):
    id: int
    name: str
    ticker: Optional[str]
    country_phone_code: Optional[str]

    class Config:
        from_attributes = True

class StateResponse(BaseModel):
    id: int
    name: str
    ticker: Optional[str]
    master_country_id: Optional[int]

    class Config:
        from_attributes = True

class CityResponse(BaseModel):
    id: int
    name: Optional[str]
    master_country_id: Optional[int]
    master_state_id: Optional[int]

    class Config:
        from_attributes = True

class CurrencyResponse(BaseModel):
    id: int
    name: Optional[str]
    ticker: Optional[str]
    icon: Optional[str]

    class Config:
        from_attributes = True

class LanguageResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class TimeZoneResponse(BaseModel):
    id: int
    timezone_name: str
    utc_offset_minutes: int
    is_default: bool

    class Config:
        from_attributes = True

class HubResponse(BaseModel):
    id: int
    name: Optional[str]
    country_name: Optional[str]
    state_name: Optional[str]
    city_name: Optional[str]
    is_active_or_planning: bool

    class Config:
        from_attributes = True

class AIModelResponse(BaseModel):
    id: int
    model_name: str
    provider_name: str
    model_version: Optional[str]
    is_active: bool
    display_sequence: int

    class Config:
        from_attributes = True

class AIPromptResponse(BaseModel):
    id: int
    title: str
    category: Optional[str]
    is_published: bool
    is_system_template: bool
    usage_count: int

    class Config:
        from_attributes = True

class DurationTypeResponse(BaseModel):
    id: int
    name: str
    number_of_days: Optional[int]
    display_sequence: int

    class Config:
        from_attributes = True

class SubscriptionTypeResponse(BaseModel):
    id: int
    name: str
    price: Optional[str]
    master_currency_id: str
    is_active: bool
    display_sequence: int

    class Config:
        from_attributes = True

class TagGroupResponse(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]
    is_public_or_private_tag: bool

    class Config:
        from_attributes = True

class TagCategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    master_tag_group_id: Optional[int]

    class Config:
        from_attributes = True

class TagResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    synonyms: Optional[str]
    master_tag_group_id: Optional[int]
    master_tag_category_id: Optional[int]

    class Config:
        from_attributes = True

class GeoFilterRequest(BaseModel):
    country_id: Optional[int] = None
    state_id: Optional[int] = None

class TagSearchRequest(BaseModel):
    query: str
    group_id: Optional[int] = None
    category_id: Optional[int] = None
