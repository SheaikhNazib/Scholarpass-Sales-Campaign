from abc import ABC, abstractmethod
from typing import Optional, List
from src.modules.user.models import AppUser, AppRole, UserRole

class IUserRepository(ABC):
    @abstractmethod
    def create(self, user: AppUser) -> AppUser:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[AppUser]:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[AppUser]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[AppUser]:
        pass

    @abstractmethod
    def update(self, user_id: int, **kwargs) -> Optional[AppUser]:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def list_all(self, skip: int = 0, limit: int = 10) -> List[AppUser]:
        pass

class IRoleRepository(ABC):
    @abstractmethod
    def create(self, role: AppRole) -> AppRole:
        pass

    @abstractmethod
    def get_by_id(self, role_id: int) -> Optional[AppRole]:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[AppRole]:
        pass

    @abstractmethod
    def list_all(self) -> List[AppRole]:
        pass

class IUserRoleRepository(ABC):
    @abstractmethod
    def assign_role(self, user_role: UserRole) -> UserRole:
        pass

    @abstractmethod
    def get_user_roles(self, user_id: int) -> List[UserRole]:
        pass

    @abstractmethod
    def remove_role(self, user_id: int, role_id: int) -> bool:
        pass

class IAccessRepository(ABC):
    @abstractmethod
    def get_user_permissions(self, user_id: int) -> List:
        pass

    @abstractmethod
    def get_user_menus(self, user_id: int) -> List:
        pass

    @abstractmethod
    def has_permission(self, user_id: int, permission_key: str) -> bool:
        pass

class IUserDeviceRepository(ABC):
    @abstractmethod
    def create(self, device) -> object:
        pass

    @abstractmethod
    def get_by_user(self, user_id: int) -> List:
        pass

    @abstractmethod
    def update_last_login(self, device_id: int) -> object:
        pass

class IUserContactRepository(ABC):
    @abstractmethod
    def create(self, contact) -> object:
        pass

    @abstractmethod
    def get_by_user(self, user_id: int) -> List:
        pass

    @abstractmethod
    def get_primary(self, user_id: int, channel_type: str) -> Optional[object]:
        pass

    @abstractmethod
    def verify_contact(self, contact_id: int) -> object:
        pass

class IUserAddressRepository(ABC):
    @abstractmethod
    def create(self, address) -> object:
        pass

    @abstractmethod
    def get_by_user(self, user_id: int) -> List:
        pass

    @abstractmethod
    def get_primary(self, user_id: int) -> Optional[object]:
        pass

    @abstractmethod
    def update(self, address_id: int, **kwargs) -> Optional[object]:
        pass

class IUserSubscriptionRepository(ABC):
    @abstractmethod
    def create(self, subscription) -> object:
        pass

    @abstractmethod
    def get_active(self, user_id: int) -> Optional[object]:
        pass

    @abstractmethod
    def cancel(self, subscription_id: int, reason: str) -> object:
        pass

class IUserPaymentRepository(ABC):
    @abstractmethod
    def create_method(self, payment_method) -> object:
        pass

    @abstractmethod
    def get_methods(self, user_id: int) -> List:
        pass

    @abstractmethod
    def record_transaction(self, transaction) -> object:
        pass

    @abstractmethod
    def get_history(self, user_id: int, limit: int = 20) -> List:
        pass

class IUserTagRepository(ABC):
    @abstractmethod
    def create(self, tag) -> object:
        pass

    @abstractmethod
    def get_by_user(self, user_id: int) -> List:
        pass

    @abstractmethod
    def verify_tag(self, tag_id: int) -> object:
        pass

    @abstractmethod
    def get_completion_tracking(self, user_id: int) -> List:
        pass
