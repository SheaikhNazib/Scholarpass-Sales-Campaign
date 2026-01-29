from typing import Optional, List, Protocol
from sqlalchemy.orm import Session
from datetime import datetime
from src.modules.contract.models import (
    CRMContract, CRMContractTerm, CRMContractMultiplePartiesSign,
    CRMContractTrackerTaskReminder
)

class ICRMContractRepository(Protocol):
    def create(self, contract: CRMContract) -> CRMContract: ...
    def get_by_id(self, contract_id: int) -> Optional[CRMContract]: ...
    def list_all(self, limit: int = 20) -> List[CRMContract]: ...
    def list_active(self, limit: int = 20) -> List[CRMContract]: ...
    def update(self, contract_id: int, **kwargs) -> Optional[CRMContract]: ...
    def delete(self, contract_id: int) -> bool: ...

class ICRMContractTermRepository(Protocol):
    def create(self, term: CRMContractTerm) -> CRMContractTerm: ...
    def get_by_id(self, term_id: int) -> Optional[CRMContractTerm]: ...
    def list_by_contract(self, contract_id: int) -> List[CRMContractTerm]: ...
    def update(self, term_id: int, **kwargs) -> Optional[CRMContractTerm]: ...
    def delete(self, term_id: int) -> bool: ...

class ICRMContractSignRepository(Protocol):
    def create(self, sign: CRMContractMultiplePartiesSign) -> CRMContractMultiplePartiesSign: ...
    def get_by_id(self, sign_id: int) -> Optional[CRMContractMultiplePartiesSign]: ...
    def list_by_contract(self, contract_id: int) -> List[CRMContractMultiplePartiesSign]: ...
    def list_unsigned(self, contract_id: int) -> List[CRMContractMultiplePartiesSign]: ...
    def update(self, sign_id: int, **kwargs) -> Optional[CRMContractMultiplePartiesSign]: ...

class ICRMContractReminderRepository(Protocol):
    def create(self, reminder: CRMContractTrackerTaskReminder) -> CRMContractTrackerTaskReminder: ...
    def get_by_id(self, reminder_id: int) -> Optional[CRMContractTrackerTaskReminder]: ...
    def list_by_contract(self, contract_id: int, limit: int = 20) -> List[CRMContractTrackerTaskReminder]: ...
    def list_pending(self) -> List[CRMContractTrackerTaskReminder]: ...
    def update(self, reminder_id: int, **kwargs) -> Optional[CRMContractTrackerTaskReminder]: ...

class CRMContractRepository(ICRMContractRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, contract: CRMContract) -> CRMContract:
        self.db.add(contract)
        self.db.commit()
        self.db.refresh(contract)
        return contract

    def get_by_id(self, contract_id: int) -> Optional[CRMContract]:
        return self.db.query(CRMContract).filter(CRMContract.id == contract_id).first()

    def list_all(self, limit: int = 20) -> List[CRMContract]:
        return self.db.query(CRMContract).order_by(CRMContract.created_at.desc()).limit(limit).all()

    def list_active(self, limit: int = 20) -> List[CRMContract]:
        return self.db.query(CRMContract).filter(
            CRMContract.active_or_expired == True,
            CRMContract.deleted_at == None
        ).order_by(CRMContract.created_at.desc()).limit(limit).all()

    def update(self, contract_id: int, **kwargs) -> Optional[CRMContract]:
        contract = self.get_by_id(contract_id)
        if contract:
            for key, value in kwargs.items():
                setattr(contract, key, value)
            self.db.commit()
            self.db.refresh(contract)
        return contract

    def delete(self, contract_id: int) -> bool:
        contract = self.get_by_id(contract_id)
        if contract:
            contract.deleted_at = datetime.utcnow()
            self.db.commit()
            return True
        return False

class CRMContractTermRepository(ICRMContractTermRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, term: CRMContractTerm) -> CRMContractTerm:
        self.db.add(term)
        self.db.commit()
        self.db.refresh(term)
        return term

    def get_by_id(self, term_id: int) -> Optional[CRMContractTerm]:
        return self.db.query(CRMContractTerm).filter(CRMContractTerm.id == term_id).first()

    def list_by_contract(self, contract_id: int) -> List[CRMContractTerm]:
        return self.db.query(CRMContractTerm).filter(
            CRMContractTerm.contract_id == contract_id
        ).all()

    def update(self, term_id: int, **kwargs) -> Optional[CRMContractTerm]:
        term = self.get_by_id(term_id)
        if term:
            for key, value in kwargs.items():
                setattr(term, key, value)
            self.db.commit()
            self.db.refresh(term)
        return term

    def delete(self, term_id: int) -> bool:
        term = self.get_by_id(term_id)
        if term:
            self.db.delete(term)
            self.db.commit()
            return True
        return False

class CRMContractSignRepository(ICRMContractSignRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, sign: CRMContractMultiplePartiesSign) -> CRMContractMultiplePartiesSign:
        self.db.add(sign)
        self.db.commit()
        self.db.refresh(sign)
        return sign

    def get_by_id(self, sign_id: int) -> Optional[CRMContractMultiplePartiesSign]:
        return self.db.query(CRMContractMultiplePartiesSign).filter(CRMContractMultiplePartiesSign.id == sign_id).first()

    def list_by_contract(self, contract_id: int) -> List[CRMContractMultiplePartiesSign]:
        return self.db.query(CRMContractMultiplePartiesSign).filter(
            CRMContractMultiplePartiesSign.contract_id == contract_id
        ).all()

    def list_unsigned(self, contract_id: int) -> List[CRMContractMultiplePartiesSign]:
        return self.db.query(CRMContractMultiplePartiesSign).filter(
            CRMContractMultiplePartiesSign.contract_id == contract_id,
            CRMContractMultiplePartiesSign.signed == False
        ).all()

    def update(self, sign_id: int, **kwargs) -> Optional[CRMContractMultiplePartiesSign]:
        sign = self.get_by_id(sign_id)
        if sign:
            for key, value in kwargs.items():
                setattr(sign, key, value)
            self.db.commit()
            self.db.refresh(sign)
        return sign

class CRMContractReminderRepository(ICRMContractReminderRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, reminder: CRMContractTrackerTaskReminder) -> CRMContractTrackerTaskReminder:
        self.db.add(reminder)
        self.db.commit()
        self.db.refresh(reminder)
        return reminder

    def get_by_id(self, reminder_id: int) -> Optional[CRMContractTrackerTaskReminder]:
        return self.db.query(CRMContractTrackerTaskReminder).filter(CRMContractTrackerTaskReminder.id == reminder_id).first()

    def list_by_contract(self, contract_id: int, limit: int = 20) -> List[CRMContractTrackerTaskReminder]:
        return self.db.query(CRMContractTrackerTaskReminder).filter(
            CRMContractTrackerTaskReminder.contract_id == contract_id
        ).order_by(CRMContractTrackerTaskReminder.due_date.desc()).limit(limit).all()

    def list_pending(self) -> List[CRMContractTrackerTaskReminder]:
        return self.db.query(CRMContractTrackerTaskReminder).filter(
            CRMContractTrackerTaskReminder.completed == False,
            CRMContractTrackerTaskReminder.due_date <= datetime.utcnow()
        ).all()

    def update(self, reminder_id: int, **kwargs) -> Optional[CRMContractTrackerTaskReminder]:
        reminder = self.get_by_id(reminder_id)
        if reminder:
            for key, value in kwargs.items():
                setattr(reminder, key, value)
            self.db.commit()
            self.db.refresh(reminder)
        return reminder
