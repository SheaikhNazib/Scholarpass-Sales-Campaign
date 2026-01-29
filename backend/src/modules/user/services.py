from typing import Optional
from src.infrastructure.security import SecurityService
from src.modules.user.adapters import UserRepository, RoleRepository, UserRoleRepository
from src.modules.user.models import AppUser, UserRole
from src.modules.user.schemas import UserRegisterRequest, UserLoginRequest, TokenResponse, UserResponse
from sqlalchemy.orm import Session

class AuthService:
    def __init__(self, user_repo: UserRepository, db: Session):
        self.user_repo = user_repo
        self.db = db

    def register(self, req: UserRegisterRequest) -> UserResponse:
        existing = self.user_repo.get_by_email(req.email)
        if existing:
            raise ValueError("Email already registered")
        
        user = AppUser(
            username=req.username,
            email=req.email,
            password_hash=SecurityService.hash_password(req.password),
            first_name=req.first_name,
            last_name=req.last_name,
            primary_role_id=3
        )
        created = self.user_repo.create(user)
        return UserResponse.from_orm(created)

    def login(self, req: UserLoginRequest) -> TokenResponse:
        user = self.user_repo.get_by_username(req.username)
        if not user or not SecurityService.verify_password(req.password, user.password_hash):
            raise ValueError("Invalid credentials")
        
        if not user.active_or_archive:
            raise ValueError("User account is inactive")
        
        token = SecurityService.create_token({"sub": str(user.id), "username": user.username})
        return TokenResponse(
            access_token=token,
            user=UserResponse.from_orm(user)
        )

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_user(self, user_id: int) -> Optional[UserResponse]:
        user = self.user_repo.get_by_id(user_id)
        return UserResponse.from_orm(user) if user else None

    def update_user(self, user_id: int, **kwargs) -> Optional[UserResponse]:
        user = self.user_repo.update(user_id, **kwargs)
        return UserResponse.from_orm(user) if user else None

    def list_users(self, skip: int = 0, limit: int = 10):
        return self.user_repo.list_all(skip, limit)

class RoleService:
    def __init__(self, role_repo: RoleRepository):
        self.role_repo = role_repo

    def get_all_roles(self):
        return self.role_repo.list_all()

class UserRoleService:
    def __init__(self, user_role_repo: UserRoleRepository):
        self.user_role_repo = user_role_repo

    def assign_role(self, user_id: int, role_id: int, assigned_by: int):
        user_role = UserRole(
            user_id=user_id,
            role_id=role_id,
            assigned_by_user_id=assigned_by
        )
        return self.user_role_repo.assign_role(user_role)

    def get_user_roles(self, user_id: int):
        return self.user_role_repo.get_user_roles(user_id)

    def remove_role(self, user_id: int, role_id: int) -> bool:
        return self.user_role_repo.remove_role(user_id, role_id)
