from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.infrastructure.auth import get_current_user
from src.modules.user.adapters import (
    AccessRepository, UserDeviceRepository, UserContactRepository,
    UserAddressRepository, UserSubscriptionRepository, UserPaymentRepository,
    UserTagRepository
)
from src.modules.access.services import (
    AccessService, UserDeviceService, UserContactService, UserAddressService,
    UserSubscriptionService, UserPaymentService, UserTagService
)
from src.modules.access.schemas import (
    PermissionResponse, MenuResponse, UserDeviceRequest, UserDeviceResponse,
    UserContactRequest, UserContactResponse, UserAddressRequest, UserAddressResponse,
    UserSubscriptionRequest, UserSubscriptionResponse, UserPaymentMethodRequest,
    UserPaymentMethodResponse, UserPaymentHistoryResponse, UserTagRequest,
    UserTagResponse, UserProfileCompletionResponse, AccessCheckRequest,
    AccessCheckResponse
)

router = APIRouter(prefix="/api/access", tags=["access"])

@router.get("/permissions", response_model=list[PermissionResponse])
def get_permissions(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    service = AccessService(AccessRepository(db))
    return service.get_user_permissions(current_user.id)

@router.get("/menus", response_model=list[MenuResponse])
def get_menus(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    service = AccessService(AccessRepository(db))
    return service.get_user_menus(current_user.id)

@router.post("/check-permission", response_model=AccessCheckResponse)
def check_permission(req: AccessCheckRequest, current_user = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    service = AccessService(AccessRepository(db))
    has_access = service.has_permission(current_user.id, req.permission_key)
    return AccessCheckResponse(has_access=has_access, permission_key=req.permission_key)

@router.post("/devices", response_model=UserDeviceResponse)
def register_device(req: UserDeviceRequest, current_user = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    service = UserDeviceService(UserDeviceRepository(db))
    return service.register_device(
        current_user.id, req.device_type, req.device_os,
        req.device_browser, req.device_ip
    )

@router.get("/devices", response_model=list[UserDeviceResponse])
def get_devices(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    service = UserDeviceService(UserDeviceRepository(db))
    return service.get_user_devices(current_user.id)

@router.post("/contacts", response_model=UserContactResponse)
def add_contact(req: UserContactRequest, current_user = Depends(get_current_user),
               db: Session = Depends(get_db)):
    service = UserContactService(UserContactRepository(db))
    return service.add_contact(
        current_user.id, req.channel_type, req.contact_value, req.is_primary
    )

@router.get("/contacts", response_model=list[UserContactResponse])
def get_contacts(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    service = UserContactService(UserContactRepository(db))
    return service.get_contacts(current_user.id)

@router.post("/contacts/{contact_id}/verify", response_model=UserContactResponse)
def verify_contact(contact_id: int, current_user = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    service = UserContactService(UserContactRepository(db))
    return service.verify_contact(contact_id)

@router.post("/addresses", response_model=UserAddressResponse)
def add_address(req: UserAddressRequest, current_user = Depends(get_current_user),
               db: Session = Depends(get_db)):
    service = UserAddressService(UserAddressRepository(db))
    return service.add_address(
        current_user.id, req.address_type, req.address_line1, req.city,
        address_line2=req.address_line2, state_province=req.state_province,
        postal_code=req.postal_code, country_code=req.country_code,
        phone_number=req.phone_number, is_primary=req.is_primary
    )

@router.get("/addresses", response_model=list[UserAddressResponse])
def get_addresses(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    service = UserAddressService(UserAddressRepository(db))
    return service.get_addresses(current_user.id)

@router.put("/addresses/{address_id}", response_model=UserAddressResponse)
def update_address(address_id: int, req: UserAddressRequest,
                  current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    service = UserAddressService(UserAddressRepository(db))
    return service.update_address(address_id, **req.dict(exclude_unset=True))

@router.post("/subscriptions", response_model=UserSubscriptionResponse)
def create_subscription(req: UserSubscriptionRequest, current_user = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    service = UserSubscriptionService(UserSubscriptionRepository(db))
    return service.create_subscription(
        current_user.id, req.master_app_subscription_types_id,
        req.billing_cycle, req.amount
    )

@router.get("/subscriptions/active", response_model=UserSubscriptionResponse)
def get_active_subscription(current_user = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    service = UserSubscriptionService(UserSubscriptionRepository(db))
    subscription = service.get_active_subscription(current_user.id)
    if not subscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active subscription")
    return subscription

@router.post("/subscriptions/{subscription_id}/cancel", response_model=UserSubscriptionResponse)
def cancel_subscription(subscription_id: int, reason: str,
                       current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    service = UserSubscriptionService(UserSubscriptionRepository(db))
    return service.cancel_subscription(subscription_id, reason)

@router.post("/payment-methods", response_model=UserPaymentMethodResponse)
def add_payment_method(req: UserPaymentMethodRequest, current_user = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    service = UserPaymentService(UserPaymentRepository(db))
    return service.add_payment_method(
        current_user.id, req.payment_type, req.payment_token,
        card_last_four=req.card_last_four, card_brand=req.card_brand
    )

@router.get("/payment-methods", response_model=list[UserPaymentMethodResponse])
def get_payment_methods(current_user = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    service = UserPaymentService(UserPaymentRepository(db))
    return service.get_payment_methods(current_user.id)

@router.get("/payment-history", response_model=list[UserPaymentHistoryResponse])
def get_payment_history(limit: int = 20, current_user = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    service = UserPaymentService(UserPaymentRepository(db))
    return service.get_payment_history(current_user.id, limit)

@router.post("/tags", response_model=UserTagResponse)
def add_tag(req: UserTagRequest, current_user = Depends(get_current_user),
           db: Session = Depends(get_db)):
    service = UserTagService(UserTagRepository(db))
    return service.add_tag(
        current_user.id, req.tag_name, req.tag_value, req.source_type
    )

@router.get("/tags", response_model=list[UserTagResponse])
def get_tags(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    service = UserTagService(UserTagRepository(db))
    return service.get_user_tags(current_user.id)

@router.post("/tags/{tag_id}/verify", response_model=UserTagResponse)
def verify_tag(tag_id: int, current_user = Depends(get_current_user),
              db: Session = Depends(get_db)):
    service = UserTagService(UserTagRepository(db))
    return service.verify_tag(tag_id)

@router.get("/profile-completion", response_model=list[UserProfileCompletionResponse])
def get_profile_completion(current_user = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    service = UserTagService(UserTagRepository(db))
    return service.get_profile_completion(current_user.id)
