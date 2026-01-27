from typing import Optional, List
from datetime import datetime
from src.modules.user.adapters import (
    AccessRepository, UserDeviceRepository, UserContactRepository,
    UserAddressRepository, UserSubscriptionRepository, UserPaymentRepository,
    UserTagRepository
)
from src.modules.access.models import (
    UserDevice, UserContactInfo, UserAddress, UserSubscription,
    UserPaymentMethod, UserPaymentHistory, UserTag, UserProfileCompletion
)

class AccessService:
    def __init__(self, access_repo: AccessRepository):
        self.access_repo = access_repo

    def get_user_permissions(self, user_id: int) -> List:
        return self.access_repo.get_user_permissions(user_id)

    def get_user_menus(self, user_id: int) -> List:
        return self.access_repo.get_user_menus(user_id)

    def has_permission(self, user_id: int, permission_key: str) -> bool:
        return self.access_repo.has_permission(user_id, permission_key)

class UserDeviceService:
    def __init__(self, device_repo: UserDeviceRepository):
        self.device_repo = device_repo

    def register_device(self, user_id: int, device_type: str, device_os: str,
                       device_browser: str, device_ip: str) -> UserDevice:
        device = UserDevice(
            user_id=user_id,
            device_type=device_type,
            device_os=device_os,
            device_browser=device_browser,
            device_ip=device_ip
        )
        return self.device_repo.create(device)

    def get_user_devices(self, user_id: int) -> List[UserDevice]:
        return self.device_repo.get_by_user(user_id)

    def update_login(self, device_id: int) -> UserDevice:
        return self.device_repo.update_last_login(device_id)

class UserContactService:
    def __init__(self, contact_repo: UserContactRepository):
        self.contact_repo = contact_repo

    def add_contact(self, user_id: int, channel_type: str, contact_value: str,
                   is_primary: bool = False) -> UserContactInfo:
        contact = UserContactInfo(
            user_id=user_id,
            channel_type=channel_type,
            contact_value=contact_value,
            is_primary=is_primary
        )
        return self.contact_repo.create(contact)

    def get_contacts(self, user_id: int) -> List[UserContactInfo]:
        return self.contact_repo.get_by_user(user_id)

    def verify_contact(self, contact_id: int) -> UserContactInfo:
        return self.contact_repo.verify_contact(contact_id)

    def get_primary_contact(self, user_id: int, channel_type: str) -> Optional[UserContactInfo]:
        return self.contact_repo.get_primary(user_id, channel_type)

class UserAddressService:
    def __init__(self, address_repo: UserAddressRepository):
        self.address_repo = address_repo

    def add_address(self, user_id: int, address_type: str, address_line1: str,
                   city: str, **kwargs) -> UserAddress:
        address = UserAddress(
            user_id=user_id,
            address_type=address_type,
            address_line1=address_line1,
            city=city,
            **kwargs
        )
        return self.address_repo.create(address)

    def get_addresses(self, user_id: int) -> List[UserAddress]:
        return self.address_repo.get_by_user(user_id)

    def get_primary_address(self, user_id: int) -> Optional[UserAddress]:
        return self.address_repo.get_primary(user_id)

    def update_address(self, address_id: int, **kwargs) -> Optional[UserAddress]:
        return self.address_repo.update(address_id, **kwargs)

class UserSubscriptionService:
    def __init__(self, subscription_repo: UserSubscriptionRepository):
        self.subscription_repo = subscription_repo

    def create_subscription(self, user_id: int, subscription_type_id: int,
                          billing_cycle: str, amount: str) -> UserSubscription:
        subscription = UserSubscription(
            user_id=user_id,
            master_app_subscription_types_id=subscription_type_id,
            billing_cycle=billing_cycle,
            amount=amount
        )
        return self.subscription_repo.create(subscription)

    def get_active_subscription(self, user_id: int) -> Optional[UserSubscription]:
        return self.subscription_repo.get_active(user_id)

    def cancel_subscription(self, subscription_id: int, reason: str) -> UserSubscription:
        return self.subscription_repo.cancel(subscription_id, reason)

class UserPaymentService:
    def __init__(self, payment_repo: UserPaymentRepository):
        self.payment_repo = payment_repo

    def add_payment_method(self, user_id: int, payment_type: str,
                          payment_token: str, **kwargs) -> UserPaymentMethod:
        method = UserPaymentMethod(
            user_id=user_id,
            payment_type=payment_type,
            payment_token=payment_token,
            **kwargs
        )
        return self.payment_repo.create_method(method)

    def get_payment_methods(self, user_id: int) -> List[UserPaymentMethod]:
        return self.payment_repo.get_methods(user_id)

    def record_payment(self, user_id: int, transaction_type: str, amount: str,
                      status: str, **kwargs) -> UserPaymentHistory:
        transaction = UserPaymentHistory(
            user_id=user_id,
            transaction_type=transaction_type,
            amount=amount,
            status=status,
            processed_at=datetime.utcnow(),
            **kwargs
        )
        return self.payment_repo.record_transaction(transaction)

    def get_payment_history(self, user_id: int, limit: int = 20) -> List[UserPaymentHistory]:
        return self.payment_repo.get_history(user_id, limit)

class UserTagService:
    def __init__(self, tag_repo: UserTagRepository):
        self.tag_repo = tag_repo

    def add_tag(self, user_id: int, tag_name: str, tag_value: str = None,
               source_type: str = 'manual', **kwargs) -> UserTag:
        tag = UserTag(
            user_id=user_id,
            tag_name=tag_name,
            tag_value=tag_value,
            source_type=source_type,
            **kwargs
        )
        return self.tag_repo.create(tag)

    def get_user_tags(self, user_id: int) -> List[UserTag]:
        return self.tag_repo.get_by_user(user_id)

    def verify_tag(self, tag_id: int) -> UserTag:
        return self.tag_repo.verify_tag(tag_id)

    def get_profile_completion(self, user_id: int) -> List[UserProfileCompletion]:
        return self.tag_repo.get_completion_tracking(user_id)
