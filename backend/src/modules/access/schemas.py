from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class PermissionResponse(BaseModel):
    id: int
    name: str
    permission_key: str
    module_name: Optional[str]
    feature_name: Optional[str]

    class Config:
        from_attributes = True

class MenuResponse(BaseModel):
    id: int
    name: str
    display_name: Optional[str]
    icon: Optional[str]
    route_path: Optional[str]
    display_sequence: Optional[int]

    class Config:
        from_attributes = True

class UserDeviceRequest(BaseModel):
    device_type: str
    device_os: str
    device_browser: str
    device_ip: str

class UserDeviceResponse(BaseModel):
    id: int
    user_id: int
    device_type: str
    device_os: str
    device_browser: str
    device_ip: str
    last_login_at: datetime

    class Config:
        from_attributes = True

class UserContactRequest(BaseModel):
    channel_type: str
    contact_value: str
    is_primary: bool = False
    opt_in_marketing: bool = True
    opt_in_transactional: bool = True

class UserContactResponse(BaseModel):
    id: int
    user_id: int
    channel_type: str
    contact_value: str
    is_primary: bool
    is_verified: bool
    verified_at: Optional[datetime]

    class Config:
        from_attributes = True

class UserAddressRequest(BaseModel):
    address_type: str
    address_line1: str
    address_line2: Optional[str]
    city: str
    state_province: Optional[str]
    postal_code: Optional[str]
    country_code: Optional[str]
    phone_number: Optional[str]
    is_primary: bool = False

class UserAddressResponse(BaseModel):
    id: int
    user_id: int
    address_type: str
    address_line1: str
    city: str
    is_primary: bool
    is_verified: bool

    class Config:
        from_attributes = True

class UserSubscriptionRequest(BaseModel):
    master_app_subscription_types_id: int
    billing_cycle: str
    amount: str

class UserSubscriptionResponse(BaseModel):
    id: int
    user_id: int
    start_date: datetime
    end_date: Optional[datetime]
    auto_renew: bool
    billing_cycle: str
    amount: str

    class Config:
        from_attributes = True

class UserPaymentMethodRequest(BaseModel):
    payment_type: str
    payment_token: str
    card_last_four: Optional[str]
    card_brand: Optional[str]

class UserPaymentMethodResponse(BaseModel):
    id: int
    user_id: int
    payment_type: str
    is_primary: bool
    card_last_four: Optional[str]
    card_brand: Optional[str]

    class Config:
        from_attributes = True

class UserPaymentHistoryResponse(BaseModel):
    id: int
    user_id: int
    transaction_type: str
    amount: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserTagRequest(BaseModel):
    tag_name: str
    tag_value: Optional[str]
    source_type: str = 'manual'

class UserTagResponse(BaseModel):
    id: int
    user_id: int
    tag_name: str
    tag_value: Optional[str]
    is_verified: bool
    is_filled: bool

    class Config:
        from_attributes = True

class UserProfileCompletionResponse(BaseModel):
    id: int
    user_id: int
    profile_section: str
    completion_percentage: str
    is_complete: bool
    filled_tags_count: int
    required_tags_count: int

    class Config:
        from_attributes = True

class AccessCheckRequest(BaseModel):
    permission_key: str

class AccessCheckResponse(BaseModel):
    has_access: bool
    permission_key: str
