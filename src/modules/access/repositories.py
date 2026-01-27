from abc import ABC, abstractmethod
from typing import Optional, List
from src.modules.access.models import Permission, Menu, RoleMenuPermission

class IPermissionRepository(ABC):
    @abstractmethod
    def create(self, permission: Permission) -> Permission:
        pass

    @abstractmethod
    def get_by_id(self, perm_id: int) -> Optional[Permission]:
        pass

    @abstractmethod
    def get_by_key(self, key: str) -> Optional[Permission]:
        pass

    @abstractmethod
    def list_all(self) -> List[Permission]:
        pass

class IMenuRepository(ABC):
    @abstractmethod
    def create(self, menu: Menu) -> Menu:
        pass

    @abstractmethod
    def get_by_id(self, menu_id: int) -> Optional[Menu]:
        pass

    @abstractmethod
    def list_all(self) -> List[Menu]:
        pass

    @abstractmethod
    def get_by_parent(self, parent_id: int) -> List[Menu]:
        pass

class IRoleMenuPermissionRepository(ABC):
    @abstractmethod
    def create(self, rmp: RoleMenuPermission) -> RoleMenuPermission:
        pass

    @abstractmethod
    def get_by_role(self, role_id: int) -> List[RoleMenuPermission]:
        pass

    @abstractmethod
    def delete(self, rmp_id: int) -> bool:
        pass
