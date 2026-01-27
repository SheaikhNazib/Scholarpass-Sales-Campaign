from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.modules.contract.services import (
    CRMContractService, CRMContractTermService,
    CRMContractSignService, CRMContractReminderService
)
from src.modules.contract.repositories import (
    CRMContractRepository, CRMContractTermRepository,
    CRMContractSignRepository, CRMContractReminderRepository
)
from src.modules.contract.schemas import (
    CRMContractSchema, CRMContractTermSchema,
    CRMContractMultiplePartiesSignSchema, CRMContractTrackerTaskReminderSchema
)

router = APIRouter(prefix="/api/contracts", tags=["contracts"])

def get_contract_service(db: Session = Depends(get_db)) -> CRMContractService:
    return CRMContractService(CRMContractRepository(db))

def get_term_service(db: Session = Depends(get_db)) -> CRMContractTermService:
    return CRMContractTermService(CRMContractTermRepository(db))

def get_sign_service(db: Session = Depends(get_db)) -> CRMContractSignService:
    return CRMContractSignService(CRMContractSignRepository(db))

def get_reminder_service(db: Session = Depends(get_db)) -> CRMContractReminderService:
    return CRMContractReminderService(CRMContractReminderRepository(db))

@router.post("", response_model=CRMContractSchema, status_code=status.HTTP_201_CREATED)
def create_contract(schema: CRMContractSchema, service: CRMContractService = Depends(get_contract_service)):
    return service.create_contract(schema)

@router.get("/{contract_id}", response_model=CRMContractSchema)
def get_contract(contract_id: int, service: CRMContractService = Depends(get_contract_service)):
    contract = service.get_contract(contract_id)
    if not contract:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contract not found")
    return contract

@router.get("", response_model=list[CRMContractSchema])
def list_contracts(limit: int = 20, service: CRMContractService = Depends(get_contract_service)):
    return service.list_contracts(limit)

@router.get("/active", response_model=list[CRMContractSchema])
def list_active_contracts(limit: int = 20, service: CRMContractService = Depends(get_contract_service)):
    return service.list_active_contracts(limit)

@router.put("/{contract_id}", response_model=CRMContractSchema)
def update_contract(contract_id: int, schema: CRMContractSchema, service: CRMContractService = Depends(get_contract_service)):
    updated = service.update_contract(contract_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contract not found")
    return updated

@router.post("/{contract_id}/sign", response_model=CRMContractSchema)
def sign_contract(contract_id: int, service: CRMContractService = Depends(get_contract_service)):
    signed = service.sign_contract(contract_id)
    if not signed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contract not found")
    return signed

@router.delete("/{contract_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contract(contract_id: int, service: CRMContractService = Depends(get_contract_service)):
    if not service.delete_contract(contract_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contract not found")

@router.post("/{contract_id}/terms", response_model=CRMContractTermSchema, status_code=status.HTTP_201_CREATED)
def create_term(contract_id: int, schema: CRMContractTermSchema, service: CRMContractTermService = Depends(get_term_service)):
    schema.contract_id = contract_id
    return service.create_term(schema)

@router.get("/{contract_id}/terms/{term_id}", response_model=CRMContractTermSchema)
def get_term(contract_id: int, term_id: int, service: CRMContractTermService = Depends(get_term_service)):
    term = service.get_term(term_id)
    if not term or term.contract_id != contract_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Term not found")
    return term

@router.get("/{contract_id}/terms", response_model=list[CRMContractTermSchema])
def list_contract_terms(contract_id: int, service: CRMContractTermService = Depends(get_term_service)):
    return service.list_contract_terms(contract_id)

@router.put("/{contract_id}/terms/{term_id}", response_model=CRMContractTermSchema)
def update_term(contract_id: int, term_id: int, schema: CRMContractTermSchema, service: CRMContractTermService = Depends(get_term_service)):
    updated = service.update_term(term_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Term not found")
    return updated

@router.delete("/{contract_id}/terms/{term_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_term(contract_id: int, term_id: int, service: CRMContractTermService = Depends(get_term_service)):
    if not service.delete_term(term_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Term not found")

@router.post("/{contract_id}/signers", response_model=CRMContractMultiplePartiesSignSchema, status_code=status.HTTP_201_CREATED)
def add_signer(contract_id: int, schema: CRMContractMultiplePartiesSignSchema, service: CRMContractSignService = Depends(get_sign_service)):
    schema.contract_id = contract_id
    return service.add_signer(schema)

@router.get("/{contract_id}/signers/{signer_id}", response_model=CRMContractMultiplePartiesSignSchema)
def get_signer(contract_id: int, signer_id: int, service: CRMContractSignService = Depends(get_sign_service)):
    signer = service.get_signer(signer_id)
    if not signer or signer.contract_id != contract_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Signer not found")
    return signer

@router.get("/{contract_id}/signers", response_model=list[CRMContractMultiplePartiesSignSchema])
def list_contract_signers(contract_id: int, service: CRMContractSignService = Depends(get_sign_service)):
    return service.list_contract_signers(contract_id)

@router.get("/{contract_id}/signers/unsigned", response_model=list[CRMContractMultiplePartiesSignSchema])
def list_unsigned_signers(contract_id: int, service: CRMContractSignService = Depends(get_sign_service)):
    return service.list_unsigned_signers(contract_id)

@router.post("/{contract_id}/signers/{signer_id}/sign", response_model=CRMContractMultiplePartiesSignSchema)
def sign_document(contract_id: int, signer_id: int, signature_url: str, service: CRMContractSignService = Depends(get_sign_service)):
    signed = service.sign_document(signer_id, signature_url)
    if not signed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Signer not found")
    return signed

@router.put("/{contract_id}/signers/{signer_id}", response_model=CRMContractMultiplePartiesSignSchema)
def update_signer(contract_id: int, signer_id: int, schema: CRMContractMultiplePartiesSignSchema, service: CRMContractSignService = Depends(get_sign_service)):
    updated = service.update_signer(signer_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Signer not found")
    return updated

@router.post("/{contract_id}/reminders", response_model=CRMContractTrackerTaskReminderSchema, status_code=status.HTTP_201_CREATED)
def create_reminder(contract_id: int, schema: CRMContractTrackerTaskReminderSchema, service: CRMContractReminderService = Depends(get_reminder_service)):
    schema.contract_id = contract_id
    return service.create_reminder(schema)

@router.get("/{contract_id}/reminders/{reminder_id}", response_model=CRMContractTrackerTaskReminderSchema)
def get_reminder(contract_id: int, reminder_id: int, service: CRMContractReminderService = Depends(get_reminder_service)):
    reminder = service.get_reminder(reminder_id)
    if not reminder or reminder.contract_id != contract_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found")
    return reminder

@router.get("/{contract_id}/reminders", response_model=list[CRMContractTrackerTaskReminderSchema])
def list_contract_reminders(contract_id: int, limit: int = 20, service: CRMContractReminderService = Depends(get_reminder_service)):
    return service.list_contract_reminders(contract_id, limit)

@router.get("/reminders/pending", response_model=list[CRMContractTrackerTaskReminderSchema])
def get_pending_reminders(service: CRMContractReminderService = Depends(get_reminder_service)):
    return service.get_pending_reminders()

@router.post("/{contract_id}/reminders/{reminder_id}/complete", response_model=CRMContractTrackerTaskReminderSchema)
def complete_reminder(contract_id: int, reminder_id: int, service: CRMContractReminderService = Depends(get_reminder_service)):
    completed = service.complete_reminder(reminder_id)
    if not completed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found")
    return completed

@router.put("/{contract_id}/reminders/{reminder_id}", response_model=CRMContractTrackerTaskReminderSchema)
def update_reminder(contract_id: int, reminder_id: int, schema: CRMContractTrackerTaskReminderSchema, service: CRMContractReminderService = Depends(get_reminder_service)):
    updated = service.update_reminder(reminder_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reminder not found")
    return updated
