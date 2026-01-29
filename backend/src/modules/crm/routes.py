from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.modules.crm.services import (
    CRMCompanyService, CRMContactService, CRMGroupService,
    CRMGroupMemberService, CRMGroupMessageService
)
from src.modules.crm.repositories import (
    CRMCompanyRepository, CRMContactRepository, CRMGroupRepository,
    CRMGroupMemberRepository, CRMGroupMessageRepository
)
from src.modules.crm.schemas import (
    CRMCompanySchema, CRMContactSchema, CRMGroupSchema,
    CRMGroupMemberSchema, CRMGroupMessageSchema
)

router = APIRouter(prefix="/api/crm", tags=["crm"])

def get_company_service(db: Session = Depends(get_db)) -> CRMCompanyService:
    return CRMCompanyService(CRMCompanyRepository(db))

def get_contact_service(db: Session = Depends(get_db)) -> CRMContactService:
    return CRMContactService(CRMContactRepository(db))

def get_group_service(db: Session = Depends(get_db)) -> CRMGroupService:
    return CRMGroupService(CRMGroupRepository(db))

def get_group_member_service(db: Session = Depends(get_db)) -> CRMGroupMemberService:
    return CRMGroupMemberService(CRMGroupMemberRepository(db))

def get_group_message_service(db: Session = Depends(get_db)) -> CRMGroupMessageService:
    return CRMGroupMessageService(CRMGroupMessageRepository(db))

@router.post("/companies", response_model=CRMCompanySchema, status_code=status.HTTP_201_CREATED)
def create_company(schema: CRMCompanySchema, service: CRMCompanyService = Depends(get_company_service)):
    return service.create_company(schema)

@router.get("/companies/{company_id}", response_model=CRMCompanySchema)
def get_company(company_id: int, service: CRMCompanyService = Depends(get_company_service)):
    company = service.get_company(company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return company

@router.get("/companies", response_model=list[CRMCompanySchema])
def list_companies(limit: int = 20, service: CRMCompanyService = Depends(get_company_service)):
    return service.list_companies(limit)

@router.get("/companies/active", response_model=list[CRMCompanySchema])
def list_active_companies(limit: int = 20, service: CRMCompanyService = Depends(get_company_service)):
    return service.list_active_companies(limit)

@router.put("/companies/{company_id}", response_model=CRMCompanySchema)
def update_company(company_id: int, schema: CRMCompanySchema, service: CRMCompanyService = Depends(get_company_service)):
    updated = service.update_company(company_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return updated

@router.delete("/companies/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int, service: CRMCompanyService = Depends(get_company_service)):
    if not service.delete_company(company_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

@router.post("/contacts", response_model=CRMContactSchema, status_code=status.HTTP_201_CREATED)
def create_contact(schema: CRMContactSchema, service: CRMContactService = Depends(get_contact_service)):
    return service.create_contact(schema)

@router.get("/contacts/{contact_id}", response_model=CRMContactSchema)
def get_contact(contact_id: int, service: CRMContactService = Depends(get_contact_service)):
    contact = service.get_contact(contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.get("/contacts", response_model=list[CRMContactSchema])
def list_contacts(limit: int = 20, service: CRMContactService = Depends(get_contact_service)):
    return service.list_contacts(limit)

@router.get("/contacts/company/{company_id}", response_model=list[CRMContactSchema])
def list_company_contacts(company_id: int, limit: int = 20, service: CRMContactService = Depends(get_contact_service)):
    return service.list_company_contacts(company_id, limit)

@router.put("/contacts/{contact_id}", response_model=CRMContactSchema)
def update_contact(contact_id: int, schema: CRMContactSchema, service: CRMContactService = Depends(get_contact_service)):
    updated = service.update_contact(contact_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return updated

@router.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int, service: CRMContactService = Depends(get_contact_service)):
    if not service.delete_contact(contact_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

@router.post("/groups", response_model=CRMGroupSchema, status_code=status.HTTP_201_CREATED)
def create_group(schema: CRMGroupSchema, service: CRMGroupService = Depends(get_group_service)):
    return service.create_group(schema)

@router.get("/groups/{group_id}", response_model=CRMGroupSchema)
def get_group(group_id: int, service: CRMGroupService = Depends(get_group_service)):
    group = service.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return group

@router.get("/groups", response_model=list[CRMGroupSchema])
def list_groups(limit: int = 20, service: CRMGroupService = Depends(get_group_service)):
    return service.list_groups(limit)

@router.get("/groups/active", response_model=list[CRMGroupSchema])
def list_active_groups(limit: int = 20, service: CRMGroupService = Depends(get_group_service)):
    return service.list_active_groups(limit)

@router.put("/groups/{group_id}", response_model=CRMGroupSchema)
def update_group(group_id: int, schema: CRMGroupSchema, service: CRMGroupService = Depends(get_group_service)):
    updated = service.update_group(group_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return updated

@router.delete("/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int, service: CRMGroupService = Depends(get_group_service)):
    if not service.delete_group(group_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

@router.post("/groups/{group_id}/members", response_model=CRMGroupMemberSchema, status_code=status.HTTP_201_CREATED)
def add_group_member(group_id: int, schema: CRMGroupMemberSchema, service: CRMGroupMemberService = Depends(get_group_member_service)):
    schema.group_id = group_id
    return service.add_member(schema)

@router.get("/groups/{group_id}/members/{member_id}", response_model=CRMGroupMemberSchema)
def get_group_member(group_id: int, member_id: int, service: CRMGroupMemberService = Depends(get_group_member_service)):
    member = service.get_member(member_id)
    if not member or member.group_id != group_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    return member

@router.get("/groups/{group_id}/members", response_model=list[CRMGroupMemberSchema])
def list_group_members(group_id: int, limit: int = 20, service: CRMGroupMemberService = Depends(get_group_member_service)):
    return service.list_group_members(group_id, limit)

@router.delete("/groups/{group_id}/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_group_member(group_id: int, member_id: int, service: CRMGroupMemberService = Depends(get_group_member_service)):
    if not service.remove_member(member_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

@router.put("/groups/{group_id}/members/{member_id}", response_model=CRMGroupMemberSchema)
def update_group_member(group_id: int, member_id: int, schema: CRMGroupMemberSchema, service: CRMGroupMemberService = Depends(get_group_member_service)):
    updated = service.update_member(member_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    return updated

@router.post("/groups/{group_id}/messages", response_model=CRMGroupMessageSchema, status_code=status.HTTP_201_CREATED)
def create_group_message(group_id: int, schema: CRMGroupMessageSchema, service: CRMGroupMessageService = Depends(get_group_message_service)):
    schema.group_id = group_id
    return service.create_message(schema)

@router.get("/groups/{group_id}/messages/{message_id}", response_model=CRMGroupMessageSchema)
def get_group_message(group_id: int, message_id: int, service: CRMGroupMessageService = Depends(get_group_message_service)):
    message = service.get_message(message_id)
    if not message or message.group_id != group_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return message

@router.get("/groups/{group_id}/messages", response_model=list[CRMGroupMessageSchema])
def list_group_messages(group_id: int, limit: int = 20, service: CRMGroupMessageService = Depends(get_group_message_service)):
    return service.list_group_messages(group_id, limit)

@router.put("/groups/{group_id}/messages/{message_id}", response_model=CRMGroupMessageSchema)
def update_group_message(group_id: int, message_id: int, schema: CRMGroupMessageSchema, service: CRMGroupMessageService = Depends(get_group_message_service)):
    updated = service.update_message(message_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return updated
