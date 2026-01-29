from typing import Optional, List
from src.modules.crm.repositories import (
    CRMCompanyRepository, CRMContactRepository, CRMGroupRepository,
    CRMGroupMemberRepository, CRMGroupMessageRepository
)
from src.modules.crm.models import (
    CRMCompany, CRMContact, CRMGroup, CRMGroupMember, CRMGroupMessage
)
from src.modules.crm.schemas import (
    CRMCompanySchema, CRMContactSchema, CRMGroupSchema,
    CRMGroupMemberSchema, CRMGroupMessageSchema
)

class CRMCompanyService:
    def __init__(self, repo: CRMCompanyRepository):
        self.repo = repo

    def create_company(self, schema: CRMCompanySchema) -> CRMCompanySchema:
        company = CRMCompany(**schema.dict(exclude_unset=True))
        created = self.repo.create(company)
        return CRMCompanySchema.from_orm(created)

    def get_company(self, company_id: int) -> Optional[CRMCompanySchema]:
        company = self.repo.get_by_id(company_id)
        return CRMCompanySchema.from_orm(company) if company else None

    def list_companies(self, limit: int = 20) -> List[CRMCompanySchema]:
        companies = self.repo.list_all(limit)
        return [CRMCompanySchema.from_orm(c) for c in companies]

    def list_active_companies(self, limit: int = 20) -> List[CRMCompanySchema]:
        companies = self.repo.list_active(limit)
        return [CRMCompanySchema.from_orm(c) for c in companies]

    def update_company(self, company_id: int, schema: CRMCompanySchema) -> Optional[CRMCompanySchema]:
        updated = self.repo.update(company_id, **schema.dict(exclude_unset=True))
        return CRMCompanySchema.from_orm(updated) if updated else None

    def delete_company(self, company_id: int) -> bool:
        return self.repo.delete(company_id)

class CRMContactService:
    def __init__(self, repo: CRMContactRepository):
        self.repo = repo

    def create_contact(self, schema: CRMContactSchema) -> CRMContactSchema:
        contact = CRMContact(**schema.dict(exclude_unset=True))
        created = self.repo.create(contact)
        return CRMContactSchema.from_orm(created)

    def get_contact(self, contact_id: int) -> Optional[CRMContactSchema]:
        contact = self.repo.get_by_id(contact_id)
        return CRMContactSchema.from_orm(contact) if contact else None

    def list_contacts(self, limit: int = 20) -> List[CRMContactSchema]:
        contacts = self.repo.list_all(limit)
        return [CRMContactSchema.from_orm(c) for c in contacts]

    def list_company_contacts(self, company_id: int, limit: int = 20) -> List[CRMContactSchema]:
        contacts = self.repo.list_by_company(company_id, limit)
        return [CRMContactSchema.from_orm(c) for c in contacts]

    def update_contact(self, contact_id: int, schema: CRMContactSchema) -> Optional[CRMContactSchema]:
        updated = self.repo.update(contact_id, **schema.dict(exclude_unset=True))
        return CRMContactSchema.from_orm(updated) if updated else None

    def delete_contact(self, contact_id: int) -> bool:
        return self.repo.delete(contact_id)

class CRMGroupService:
    def __init__(self, repo: CRMGroupRepository):
        self.repo = repo

    def create_group(self, schema: CRMGroupSchema) -> CRMGroupSchema:
        group = CRMGroup(**schema.dict(exclude_unset=True))
        created = self.repo.create(group)
        return CRMGroupSchema.from_orm(created)

    def get_group(self, group_id: int) -> Optional[CRMGroupSchema]:
        group = self.repo.get_by_id(group_id)
        return CRMGroupSchema.from_orm(group) if group else None

    def list_groups(self, limit: int = 20) -> List[CRMGroupSchema]:
        groups = self.repo.list_all(limit)
        return [CRMGroupSchema.from_orm(g) for g in groups]

    def list_active_groups(self, limit: int = 20) -> List[CRMGroupSchema]:
        groups = self.repo.list_active(limit)
        return [CRMGroupSchema.from_orm(g) for g in groups]

    def update_group(self, group_id: int, schema: CRMGroupSchema) -> Optional[CRMGroupSchema]:
        updated = self.repo.update(group_id, **schema.dict(exclude_unset=True))
        return CRMGroupSchema.from_orm(updated) if updated else None

    def delete_group(self, group_id: int) -> bool:
        return self.repo.delete(group_id)

class CRMGroupMemberService:
    def __init__(self, repo: CRMGroupMemberRepository):
        self.repo = repo

    def add_member(self, schema: CRMGroupMemberSchema) -> CRMGroupMemberSchema:
        member = CRMGroupMember(**schema.dict(exclude_unset=True))
        created = self.repo.create(member)
        return CRMGroupMemberSchema.from_orm(created)

    def get_member(self, member_id: int) -> Optional[CRMGroupMemberSchema]:
        member = self.repo.get_by_id(member_id)
        return CRMGroupMemberSchema.from_orm(member) if member else None

    def list_group_members(self, group_id: int, limit: int = 20) -> List[CRMGroupMemberSchema]:
        members = self.repo.list_by_group(group_id, limit)
        return [CRMGroupMemberSchema.from_orm(m) for m in members]

    def remove_member(self, member_id: int) -> bool:
        return self.repo.remove_member(member_id)

    def update_member(self, member_id: int, schema: CRMGroupMemberSchema) -> Optional[CRMGroupMemberSchema]:
        updated = self.repo.update(member_id, **schema.dict(exclude_unset=True))
        return CRMGroupMemberSchema.from_orm(updated) if updated else None

class CRMGroupMessageService:
    def __init__(self, repo: CRMGroupMessageRepository):
        self.repo = repo

    def create_message(self, schema: CRMGroupMessageSchema) -> CRMGroupMessageSchema:
        message = CRMGroupMessage(**schema.dict(exclude_unset=True))
        created = self.repo.create(message)
        return CRMGroupMessageSchema.from_orm(created)

    def get_message(self, message_id: int) -> Optional[CRMGroupMessageSchema]:
        message = self.repo.get_by_id(message_id)
        return CRMGroupMessageSchema.from_orm(message) if message else None

    def list_group_messages(self, group_id: int, limit: int = 20) -> List[CRMGroupMessageSchema]:
        messages = self.repo.list_by_group(group_id, limit)
        return [CRMGroupMessageSchema.from_orm(m) for m in messages]

    def update_message(self, message_id: int, schema: CRMGroupMessageSchema) -> Optional[CRMGroupMessageSchema]:
        updated = self.repo.update(message_id, **schema.dict(exclude_unset=True))
        return CRMGroupMessageSchema.from_orm(updated) if updated else None
