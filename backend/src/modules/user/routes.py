from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.infrastructure.security import SecurityService
from src.modules.user.adapters import UserRepository, RoleRepository, UserRoleRepository
from src.modules.user.services import AuthService, UserService, RoleService, UserRoleService
from src.modules.user.schemas import UserRegisterRequest, UserLoginRequest, TokenResponse, UserResponse, RoleResponse

router = APIRouter(prefix="/api/v1/users", tags=["users"])

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db), db)

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))

def get_role_service(db: Session = Depends(get_db)) -> RoleService:
    return RoleService(RoleRepository(db))

def get_user_role_service(db: Session = Depends(get_db)) -> UserRoleService:
    return UserRoleService(UserRoleRepository(db))


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(req: UserRegisterRequest, service: AuthService = Depends(get_auth_service)):
    try:
        user = service.register(req)
        return user
    except ValueError as ve:
        # Domain validation errors from the service (e.g. email already registered)
        msg = str(ve) or "Invalid request"
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
    except IntegrityError as ie:
        # Database-level uniqueness/constraint errors
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Duplicate entry or constraint violation")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/login", response_model=TokenResponse)
def login(req: UserLoginRequest, service: AuthService = Depends(get_auth_service)):
    try:
        return service.login(req)
    except ValueError as ve:
        msg = str(ve) or "Invalid credentials"
        # Map authentication errors to 401/403 appropriately
        if "inactive" in msg.lower():
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=msg)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=msg)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 10, service: UserService = Depends(get_user_service)):
    return service.list_users(skip, limit)

@router.get("/roles/all", response_model=list[RoleResponse])
def get_all_roles(service: RoleService = Depends(get_role_service)):
    return service.get_all_roles()

@router.post("/{user_id}/roles/{role_id}")
def assign_role(user_id: int, role_id: int, assigned_by: int, service: UserRoleService = Depends(get_user_role_service)):
    service.assign_role(user_id, role_id, assigned_by)
    return {"message": "Role assigned successfully"}

@router.delete("/{user_id}/roles/{role_id}")
def remove_role(user_id: int, role_id: int, service: UserRoleService = Depends(get_user_role_service)):
    if not service.remove_role(user_id, role_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role assignment not found")
    return {"message": "Role removed successfully"}
