import sys
import os
# Add the parent directory of 'src' to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from src.infrastructure.database import SessionLocal
from src.infrastructure.security import SecurityService
from src.modules.user.models import AppUser, AppRole, UserRole

def seed_super_admin():
    db: Session = SessionLocal()
    try:
        # 1. Create Super Admin Role if not exists
        super_admin_role = db.query(AppRole).filter(AppRole.name == "Super Admin").first()
        if not super_admin_role:
            super_admin_role = AppRole(
                name="Super Admin",
                description="Highest level of access with all permissions",
                is_active=True,
                display_sequence=1
            )
            db.add(super_admin_role)
            db.commit()
            db.refresh(super_admin_role)
            print("Created Super Admin role")
        else:
            print(f"Super Admin role already exists with ID: {super_admin_role.id}")

        # 2. Create/Update Super Admin User
        admin_email = "admin@scholarpass.com"
        admin_username = "superadmin"
        admin_password = "AdminPassword123!"
        
        super_admin_user = db.query(AppUser).filter(AppUser.email == admin_email).first()
        
        if not super_admin_user:
            super_admin_user = AppUser(
                username=admin_username,
                email=admin_email,
                password_hash=SecurityService.hash_password(admin_password),
                first_name="Super",
                last_name="Admin",
                primary_role_id=super_admin_role.id,
                active_or_archive=True,
                email_confirmed=True
            )
            db.add(super_admin_user)
            print("Creating new Super Admin user")
        else:
            print("Updating existing Super Admin user")
            super_admin_user.username = admin_username
            super_admin_user.password_hash = SecurityService.hash_password(admin_password)
            super_admin_user.primary_role_id = super_admin_role.id
            super_admin_user.active_or_archive = True
            super_admin_user.email_confirmed = True
        
        db.commit()
        db.refresh(super_admin_user)
        print(f"Super Admin user ID: {super_admin_user.id}")

        # 3. Ensure UserRole mapping exists
        user_role_entry = db.query(UserRole).filter(
            UserRole.user_id == super_admin_user.id,
            UserRole.role_id == super_admin_role.id
        ).first()
        
        if not user_role_entry:
            user_role_entry = UserRole(
                user_id=super_admin_user.id,
                role_id=super_admin_role.id,
                is_active=True
            )
            db.add(user_role_entry)
            db.commit()
            print("Assigned Super Admin role to user in mapping table")
            
        print("\nSuccess! Final Credentials:")
        print(f"Email: {admin_email}")
        print(f"Password: {admin_password}")

    except Exception as e:
        print(f"Error seeding super admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_super_admin()
