from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
from src.modules.user.models import (
    AppUser, AppRole, UserRole, UserOTP, UserSession, UserNotification
)
from src.modules.access.models import (
    UserDevice, UserContactInfo, UserAddress, UserSubscription,
    UserPaymentMethod, UserPaymentHistory, UserTag, UserProfileCompletion,
    Permission, Menu, RoleMenuPermission
)
from src.modules.user.repositories import (
    IUserRepository, IRoleRepository, IUserRoleRepository, IAccessRepository,
    IUserDeviceRepository, IUserContactRepository, IUserAddressRepository,
    IUserSubscriptionRepository, IUserPaymentRepository, IUserTagRepository
)

class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: AppUser) -> AppUser:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[AppUser]:
        return self.db.query(AppUser).filter(AppUser.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[AppUser]:
        return self.db.query(AppUser).filter(AppUser.username == username).first()

    def get_by_email(self, email: str) -> Optional[AppUser]:
        return self.db.query(AppUser).filter(AppUser.email == email).first()

    def update(self, user_id: int, **kwargs) -> Optional[AppUser]:
        user = self.get_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False

    def list_all(self, skip: int = 0, limit: int = 10) -> List[AppUser]:
        return self.db.query(AppUser).offset(skip).limit(limit).all()

class RoleRepository(IRoleRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, role: AppRole) -> AppRole:
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def get_by_id(self, role_id: int) -> Optional[AppRole]:
        return self.db.query(AppRole).filter(AppRole.id == role_id).first()

    def get_by_name(self, name: str) -> Optional[AppRole]:
        return self.db.query(AppRole).filter(AppRole.name == name).first()

    def list_all(self) -> List[AppRole]:
        return self.db.query(AppRole).filter(AppRole.is_active == True).all()

class UserRoleRepository(IUserRoleRepository):
    def __init__(self, db: Session):
        self.db = db

    def assign_role(self, user_role: UserRole) -> UserRole:
        self.db.add(user_role)
        self.db.commit()
        self.db.refresh(user_role)
        return user_role

    def get_user_roles(self, user_id: int) -> List[UserRole]:
        return self.db.query(UserRole).filter(
            UserRole.user_id == user_id,
            UserRole.is_active == True
        ).all()

    def remove_role(self, user_id: int, role_id: int) -> bool:
        user_role = self.db.query(UserRole).filter(
            UserRole.user_id == user_id,
            UserRole.role_id == role_id
        ).first()
        if user_role:
            self.db.delete(user_role)
            self.db.commit()
            return True
        return False

class AccessRepository(IAccessRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_user_permissions(self, user_id: int) -> List:
        return self.db.query(Permission).join(
            RoleMenuPermission, Permission.id == RoleMenuPermission.permission_id
        ).join(
            AppRole, RoleMenuPermission.role_id == AppRole.id
        ).join(
            UserRole, AppRole.id == UserRole.role_id
        ).filter(UserRole.user_id == user_id, UserRole.is_active == True).all()

    def get_user_menus(self, user_id: int) -> List:
        return self.db.query(Menu).join(
            RoleMenuPermission, Menu.id == RoleMenuPermission.menu_id
        ).join(
            AppRole, RoleMenuPermission.role_id == AppRole.id
        ).join(
            UserRole, AppRole.id == UserRole.role_id
        ).filter(UserRole.user_id == user_id, UserRole.is_active == True).all()

    def has_permission(self, user_id: int, permission_key: str) -> bool:
        result = self.db.query(Permission).join(
            RoleMenuPermission, Permission.id == RoleMenuPermission.permission_id
        ).join(
            AppRole, RoleMenuPermission.role_id == AppRole.id
        ).join(
            UserRole, AppRole.id == UserRole.role_id
        ).filter(
            UserRole.user_id == user_id,
            UserRole.is_active == True,
            Permission.permission_key == permission_key
        ).first()
        return result is not None

class UserDeviceRepository(IUserDeviceRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, device: UserDevice) -> UserDevice:
        self.db.add(device)
        self.db.commit()
        self.db.refresh(device)
        return device

    def get_by_user(self, user_id: int) -> List[UserDevice]:
        return self.db.query(UserDevice).filter(UserDevice.user_id == user_id).all()

    def update_last_login(self, device_id: int) -> UserDevice:
        device = self.db.query(UserDevice).filter(UserDevice.id == device_id).first()
        if device:
            device.last_login_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(device)
        return device

class UserContactRepository(IUserContactRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, contact: UserContactInfo) -> UserContactInfo:
        self.db.add(contact)
        self.db.commit()
        self.db.refresh(contact)
        return contact

    def get_by_user(self, user_id: int) -> List[UserContactInfo]:
        return self.db.query(UserContactInfo).filter(UserContactInfo.user_id == user_id).all()

    def get_primary(self, user_id: int, channel_type: str) -> Optional[UserContactInfo]:
        return self.db.query(UserContactInfo).filter(
            UserContactInfo.user_id == user_id,
            UserContactInfo.channel_type == channel_type,
            UserContactInfo.is_primary == True
        ).first()

    def verify_contact(self, contact_id: int) -> UserContactInfo:
        contact = self.db.query(UserContactInfo).filter(UserContactInfo.id == contact_id).first()
        if contact:
            contact.is_verified = True
            contact.verified_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(contact)
        return contact

class UserAddressRepository(IUserAddressRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, address: UserAddress) -> UserAddress:
        self.db.add(address)
        self.db.commit()
        self.db.refresh(address)
        return address

    def get_by_user(self, user_id: int) -> List[UserAddress]:
        return self.db.query(UserAddress).filter(UserAddress.user_id == user_id).all()

    def get_primary(self, user_id: int) -> Optional[UserAddress]:
        return self.db.query(UserAddress).filter(
            UserAddress.user_id == user_id,
            UserAddress.is_primary == True
        ).first()

    def update(self, address_id: int, **kwargs) -> Optional[UserAddress]:
        address = self.db.query(UserAddress).filter(UserAddress.id == address_id).first()
        if address:
            for key, value in kwargs.items():
                setattr(address, key, value)
            self.db.commit()
            self.db.refresh(address)
        return address

class UserSubscriptionRepository(IUserSubscriptionRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, subscription: UserSubscription) -> UserSubscription:
        self.db.add(subscription)
        self.db.commit()
        self.db.refresh(subscription)
        return subscription

    def get_active(self, user_id: int) -> Optional[UserSubscription]:
        return self.db.query(UserSubscription).filter(
            UserSubscription.user_id == user_id,
            UserSubscription.canceled_at == None
        ).first()

    def cancel(self, subscription_id: int, reason: str) -> UserSubscription:
        subscription = self.db.query(UserSubscription).filter(UserSubscription.id == subscription_id).first()
        if subscription:
            subscription.canceled_at = datetime.utcnow()
            subscription.reason_for_cancellation = reason
            self.db.commit()
            self.db.refresh(subscription)
        return subscription

class UserPaymentRepository(IUserPaymentRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_method(self, payment_method: UserPaymentMethod) -> UserPaymentMethod:
        self.db.add(payment_method)
        self.db.commit()
        self.db.refresh(payment_method)
        return payment_method

    def get_methods(self, user_id: int) -> List[UserPaymentMethod]:
        return self.db.query(UserPaymentMethod).filter(
            UserPaymentMethod.user_id == user_id,
            UserPaymentMethod.is_active == True
        ).all()

    def record_transaction(self, transaction: UserPaymentHistory) -> UserPaymentHistory:
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def get_history(self, user_id: int, limit: int = 20) -> List[UserPaymentHistory]:
        return self.db.query(UserPaymentHistory).filter(
            UserPaymentHistory.user_id == user_id
        ).order_by(UserPaymentHistory.created_at.desc()).limit(limit).all()

class UserTagRepository(IUserTagRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, tag: UserTag) -> UserTag:
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def get_by_user(self, user_id: int) -> List[UserTag]:
        return self.db.query(UserTag).filter(UserTag.user_id == user_id).all()

    def verify_tag(self, tag_id: int) -> UserTag:
        tag = self.db.query(UserTag).filter(UserTag.id == tag_id).first()
        if tag:
            tag.is_verified = True
            tag.verified_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(tag)
        return tag

    def get_completion_tracking(self, user_id: int) -> List[UserProfileCompletion]:
        return self.db.query(UserProfileCompletion).filter(
            UserProfileCompletion.user_id == user_id
        ).all()
