from typing import Optional, List, Protocol
from sqlalchemy.orm import Session
from datetime import datetime
from src.modules.crm.models import (
    CRMCompany, CRMContact, CRMGroup, CRMGroupMember, CRMGroupMessage,
    CRMCompanyContactMap, CRMNote, CRMBankInfo
)

class ICRMCompanyRepository(Protocol):
    def create(self, company: CRMCompany) -> CRMCompany: ...
    def get_by_id(self, company_id: int) -> Optional[CRMCompany]: ...
    def list_all(self, limit: int = 20) -> List[CRMCompany]: ...
    def list_active(self, limit: int = 20) -> List[CRMCompany]: ...
    def update(self, company_id: int, **kwargs) -> Optional[CRMCompany]: ...
    def delete(self, company_id: int) -> bool: ...

class ICRMContactRepository(Protocol):
    def create(self, contact: CRMContact) -> CRMContact: ...
    def get_by_id(self, contact_id: int) -> Optional[CRMContact]: ...
    def list_all(self, limit: int = 20) -> List[CRMContact]: ...
    def list_by_company(self, company_id: int, limit: int = 20) -> List[CRMContact]: ...
    def update(self, contact_id: int, **kwargs) -> Optional[CRMContact]: ...
    def delete(self, contact_id: int) -> bool: ...

class ICRMGroupRepository(Protocol):
    def create(self, group: CRMGroup) -> CRMGroup: ...
    def get_by_id(self, group_id: int) -> Optional[CRMGroup]: ...
    def list_all(self, limit: int = 20) -> List[CRMGroup]: ...
    def list_active(self, limit: int = 20) -> List[CRMGroup]: ...
    def update(self, group_id: int, **kwargs) -> Optional[CRMGroup]: ...
    def delete(self, group_id: int) -> bool: ...

class ICRMGroupMemberRepository(Protocol):
    def create(self, member: CRMGroupMember) -> CRMGroupMember: ...
    def get_by_id(self, member_id: int) -> Optional[CRMGroupMember]: ...
    def list_by_group(self, group_id: int, limit: int = 20) -> List[CRMGroupMember]: ...
    def remove_member(self, member_id: int) -> bool: ...
    def update(self, member_id: int, **kwargs) -> Optional[CRMGroupMember]: ...

class ICRMGroupMessageRepository(Protocol):
    def create(self, message: CRMGroupMessage) -> CRMGroupMessage: ...
    def get_by_id(self, message_id: int) -> Optional[CRMGroupMessage]: ...
    def list_by_group(self, group_id: int, limit: int = 20) -> List[CRMGroupMessage]: ...
    def update(self, message_id: int, **kwargs) -> Optional[CRMGroupMessage]: ...

class CRMCompanyRepository(ICRMCompanyRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, company: CRMCompany) -> CRMCompany:
        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        return company

    def get_by_id(self, company_id: int) -> Optional[CRMCompany]:
        return self.db.query(CRMCompany).filter(CRMCompany.id == company_id).first()

    def list_all(self, limit: int = 20) -> List[CRMCompany]:
        return self.db.query(CRMCompany).order_by(CRMCompany.created_at.desc()).limit(limit).all()

    def list_active(self, limit: int = 20) -> List[CRMCompany]:
        return self.db.query(CRMCompany).filter(
            CRMCompany.is_active_or_archived == True
        ).order_by(CRMCompany.created_at.desc()).limit(limit).all()

    def update(self, company_id: int, **kwargs) -> Optional[CRMCompany]:
        company = self.get_by_id(company_id)
        if company:
            for key, value in kwargs.items():
                setattr(company, key, value)
            self.db.commit()
            self.db.refresh(company)
        return company

    def delete(self, company_id: int) -> bool:
        company = self.get_by_id(company_id)
        if company:
            self.db.delete(company)
            self.db.commit()
            return True
        return False

class CRMContactRepository(ICRMContactRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, contact: CRMContact) -> CRMContact:
        self.db.add(contact)
        self.db.commit()
        self.db.refresh(contact)
        return contact

    def get_by_id(self, contact_id: int) -> Optional[CRMContact]:
        return self.db.query(CRMContact).filter(CRMContact.id == contact_id).first()

    def list_all(self, limit: int = 20) -> List[CRMContact]:
        return self.db.query(CRMContact).order_by(CRMContact.created_at.desc()).limit(limit).all()

    def list_by_company(self, company_id: int, limit: int = 20) -> List[CRMContact]:
        return self.db.query(CRMContact).filter(
            CRMContact.company_id == company_id
        ).order_by(CRMContact.created_at.desc()).limit(limit).all()

    def update(self, contact_id: int, **kwargs) -> Optional[CRMContact]:
        contact = self.get_by_id(contact_id)
        if contact:
            for key, value in kwargs.items():
                setattr(contact, key, value)
            self.db.commit()
            self.db.refresh(contact)
        return contact

    def delete(self, contact_id: int) -> bool:
        contact = self.get_by_id(contact_id)
        if contact:
            self.db.delete(contact)
            self.db.commit()
            return True
        return False

class CRMGroupRepository(ICRMGroupRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, group: CRMGroup) -> CRMGroup:
        self.db.add(group)
        self.db.commit()
        self.db.refresh(group)
        return group

    def get_by_id(self, group_id: int) -> Optional[CRMGroup]:
        return self.db.query(CRMGroup).filter(CRMGroup.id == group_id).first()

    def list_all(self, limit: int = 20) -> List[CRMGroup]:
        return self.db.query(CRMGroup).order_by(CRMGroup.created_at.desc()).limit(limit).all()

    def list_active(self, limit: int = 20) -> List[CRMGroup]:
        return self.db.query(CRMGroup).filter(
            CRMGroup.is_active == True
        ).order_by(CRMGroup.created_at.desc()).limit(limit).all()

    def update(self, group_id: int, **kwargs) -> Optional[CRMGroup]:
        group = self.get_by_id(group_id)
        if group:
            for key, value in kwargs.items():
                setattr(group, key, value)
            self.db.commit()
            self.db.refresh(group)
        return group

    def delete(self, group_id: int) -> bool:
        group = self.get_by_id(group_id)
        if group:
            self.db.delete(group)
            self.db.commit()
            return True
        return False

class CRMGroupMemberRepository(ICRMGroupMemberRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, member: CRMGroupMember) -> CRMGroupMember:
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def get_by_id(self, member_id: int) -> Optional[CRMGroupMember]:
        return self.db.query(CRMGroupMember).filter(CRMGroupMember.id == member_id).first()

    def list_by_group(self, group_id: int, limit: int = 20) -> List[CRMGroupMember]:
        return self.db.query(CRMGroupMember).filter(
            CRMGroupMember.group_id == group_id,
            CRMGroupMember.is_active == True
        ).order_by(CRMGroupMember.joined_at.desc()).limit(limit).all()

    def remove_member(self, member_id: int) -> bool:
        member = self.get_by_id(member_id)
        if member:
            member.is_active = False
            member.removed_at = datetime.utcnow()
            self.db.commit()
            return True
        return False

    def update(self, member_id: int, **kwargs) -> Optional[CRMGroupMember]:
        member = self.get_by_id(member_id)
        if member:
            for key, value in kwargs.items():
                setattr(member, key, value)
            self.db.commit()
            self.db.refresh(member)
        return member

class CRMGroupMessageRepository(ICRMGroupMessageRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, message: CRMGroupMessage) -> CRMGroupMessage:
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_by_id(self, message_id: int) -> Optional[CRMGroupMessage]:
        return self.db.query(CRMGroupMessage).filter(CRMGroupMessage.id == message_id).first()

    def list_by_group(self, group_id: int, limit: int = 20) -> List[CRMGroupMessage]:
        return self.db.query(CRMGroupMessage).filter(
            CRMGroupMessage.group_id == group_id
        ).order_by(CRMGroupMessage.created_at.desc()).limit(limit).all()

    def update(self, message_id: int, **kwargs) -> Optional[CRMGroupMessage]:
        message = self.get_by_id(message_id)
        if message:
            for key, value in kwargs.items():
                setattr(message, key, value)
            self.db.commit()
            self.db.refresh(message)
        return message
