from typing import Optional, List
from src.modules.contract.repositories import (
    CRMContractRepository, CRMContractTermRepository,
    CRMContractSignRepository, CRMContractReminderRepository
)
from src.modules.contract.models import (
    CRMContract, CRMContractTerm, CRMContractMultiplePartiesSign,
    CRMContractTrackerTaskReminder
)
from src.modules.contract.schemas import (
    CRMContractSchema, CRMContractTermSchema,
    CRMContractMultiplePartiesSignSchema, CRMContractTrackerTaskReminderSchema
)
from datetime import datetime

class CRMContractService:
    def __init__(self, repo: CRMContractRepository):
        self.repo = repo

    def create_contract(self, schema: CRMContractSchema) -> CRMContractSchema:
        contract = CRMContract(**schema.dict(exclude_unset=True))
        created = self.repo.create(contract)
        return CRMContractSchema.from_orm(created)

    def get_contract(self, contract_id: int) -> Optional[CRMContractSchema]:
        contract = self.repo.get_by_id(contract_id)
        return CRMContractSchema.from_orm(contract) if contract else None

    def list_contracts(self, limit: int = 20) -> List[CRMContractSchema]:
        contracts = self.repo.list_all(limit)
        return [CRMContractSchema.from_orm(c) for c in contracts]

    def list_active_contracts(self, limit: int = 20) -> List[CRMContractSchema]:
        contracts = self.repo.list_active(limit)
        return [CRMContractSchema.from_orm(c) for c in contracts]

    def update_contract(self, contract_id: int, schema: CRMContractSchema) -> Optional[CRMContractSchema]:
        updated = self.repo.update(contract_id, **schema.dict(exclude_unset=True))
        return CRMContractSchema.from_orm(updated) if updated else None

    def sign_contract(self, contract_id: int) -> Optional[CRMContractSchema]:
        return self.update_contract(contract_id, CRMContractSchema(
            signed_and_completed=True,
            signed_date=datetime.utcnow()
        ))

    def delete_contract(self, contract_id: int) -> bool:
        return self.repo.delete(contract_id)

class CRMContractTermService:
    def __init__(self, repo: CRMContractTermRepository):
        self.repo = repo

    def create_term(self, schema: CRMContractTermSchema) -> CRMContractTermSchema:
        term = CRMContractTerm(**schema.dict(exclude_unset=True))
        created = self.repo.create(term)
        return CRMContractTermSchema.from_orm(created)

    def get_term(self, term_id: int) -> Optional[CRMContractTermSchema]:
        term = self.repo.get_by_id(term_id)
        return CRMContractTermSchema.from_orm(term) if term else None

    def list_contract_terms(self, contract_id: int) -> List[CRMContractTermSchema]:
        terms = self.repo.list_by_contract(contract_id)
        return [CRMContractTermSchema.from_orm(t) for t in terms]

    def update_term(self, term_id: int, schema: CRMContractTermSchema) -> Optional[CRMContractTermSchema]:
        updated = self.repo.update(term_id, **schema.dict(exclude_unset=True))
        return CRMContractTermSchema.from_orm(updated) if updated else None

    def delete_term(self, term_id: int) -> bool:
        return self.repo.delete(term_id)

class CRMContractSignService:
    def __init__(self, repo: CRMContractSignRepository):
        self.repo = repo

    def add_signer(self, schema: CRMContractMultiplePartiesSignSchema) -> CRMContractMultiplePartiesSignSchema:
        sign = CRMContractMultiplePartiesSign(**schema.dict(exclude_unset=True))
        created = self.repo.create(sign)
        return CRMContractMultiplePartiesSignSchema.from_orm(created)

    def get_signer(self, sign_id: int) -> Optional[CRMContractMultiplePartiesSignSchema]:
        sign = self.repo.get_by_id(sign_id)
        return CRMContractMultiplePartiesSignSchema.from_orm(sign) if sign else None

    def list_contract_signers(self, contract_id: int) -> List[CRMContractMultiplePartiesSignSchema]:
        signers = self.repo.list_by_contract(contract_id)
        return [CRMContractMultiplePartiesSignSchema.from_orm(s) for s in signers]

    def list_unsigned_signers(self, contract_id: int) -> List[CRMContractMultiplePartiesSignSchema]:
        signers = self.repo.list_unsigned(contract_id)
        return [CRMContractMultiplePartiesSignSchema.from_orm(s) for s in signers]

    def sign_document(self, sign_id: int, signature_url: str) -> Optional[CRMContractMultiplePartiesSignSchema]:
        updated = self.repo.update(sign_id, signed=True, sign_date_time=datetime.utcnow(), signature_image_url=signature_url)
        return CRMContractMultiplePartiesSignSchema.from_orm(updated) if updated else None

    def update_signer(self, sign_id: int, schema: CRMContractMultiplePartiesSignSchema) -> Optional[CRMContractMultiplePartiesSignSchema]:
        updated = self.repo.update(sign_id, **schema.dict(exclude_unset=True))
        return CRMContractMultiplePartiesSignSchema.from_orm(updated) if updated else None

class CRMContractReminderService:
    def __init__(self, repo: CRMContractReminderRepository):
        self.repo = repo

    def create_reminder(self, schema: CRMContractTrackerTaskReminderSchema) -> CRMContractTrackerTaskReminderSchema:
        reminder = CRMContractTrackerTaskReminder(**schema.dict(exclude_unset=True))
        created = self.repo.create(reminder)
        return CRMContractTrackerTaskReminderSchema.from_orm(created)

    def get_reminder(self, reminder_id: int) -> Optional[CRMContractTrackerTaskReminderSchema]:
        reminder = self.repo.get_by_id(reminder_id)
        return CRMContractTrackerTaskReminderSchema.from_orm(reminder) if reminder else None

    def list_contract_reminders(self, contract_id: int, limit: int = 20) -> List[CRMContractTrackerTaskReminderSchema]:
        reminders = self.repo.list_by_contract(contract_id, limit)
        return [CRMContractTrackerTaskReminderSchema.from_orm(r) for r in reminders]

    def get_pending_reminders(self) -> List[CRMContractTrackerTaskReminderSchema]:
        reminders = self.repo.list_pending()
        return [CRMContractTrackerTaskReminderSchema.from_orm(r) for r in reminders]

    def complete_reminder(self, reminder_id: int) -> Optional[CRMContractTrackerTaskReminderSchema]:
        updated = self.repo.update(reminder_id, completed=True, completed_date=datetime.utcnow())
        return CRMContractTrackerTaskReminderSchema.from_orm(updated) if updated else None

    def update_reminder(self, reminder_id: int, schema: CRMContractTrackerTaskReminderSchema) -> Optional[CRMContractTrackerTaskReminderSchema]:
        updated = self.repo.update(reminder_id, **schema.dict(exclude_unset=True))
        return CRMContractTrackerTaskReminderSchema.from_orm(updated) if updated else None
