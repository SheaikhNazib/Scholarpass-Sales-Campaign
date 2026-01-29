from typing import Optional, List
from sqlalchemy.orm import Session
from src.modules.access.models import Permission, Menu, RoleMenuPermission
from src.modules.access.repositories import IPermissionRepository, IMenuRepository, IRoleMenuPermissionRepository

class PermissionRepository(IPermissionRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, permission: Permission) -> Permission:
        self.db.add(permission)
        self.db.commit()
        self.db.refresh(permission)
        return permission

    def get_by_id(self, perm_id: int) -> Optional[Permission]:
        return self.db.query(Permission).filter(Permission.id == perm_id).first()

    def get_by_key(self, key: str) -> Optional[Permission]:
        return self.db.query(Permission).filter(Permission.permission_key == key).first()

    def list_all(self) -> List[Permission]:
        return self.db.query(Permission).all()

class MenuRepository(IMenuRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, menu: Menu) -> Menu:
        self.db.add(menu)
        self.db.commit()
        self.db.refresh(menu)
        return menu

    def get_by_id(self, menu_id: int) -> Optional[Menu]:
        return self.db.query(Menu).filter(Menu.id == menu_id).first()

    def list_all(self) -> List[Menu]:
        return self.db.query(Menu).filter(Menu.has_parent == False).all()

    def get_by_parent(self, parent_id: int) -> List[Menu]:
        return self.db.query(Menu).filter(Menu.parent_menu_id == parent_id).all()

class RoleMenuPermissionRepository(IRoleMenuPermissionRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, rmp: RoleMenuPermission) -> RoleMenuPermission:
        self.db.add(rmp)
        self.db.commit()
        self.db.refresh(rmp)
        return rmp

    def get_by_role(self, role_id: int) -> List[RoleMenuPermission]:
        return self.db.query(RoleMenuPermission).filter(RoleMenuPermission.role_id == role_id).all()

    def delete(self, rmp_id: int) -> bool:
        rmp = self.db.query(RoleMenuPermission).filter(RoleMenuPermission.id == rmp_id).first()
        if rmp:
            self.db.delete(rmp)
            self.db.commit()
            return True
        return False
