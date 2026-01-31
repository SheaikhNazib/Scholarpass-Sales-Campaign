from typing import Optional, List, Protocol
from sqlalchemy.orm import Session
from datetime import datetime
from src.modules.sales.models import (
    CRMSalesCampaign, CRMSalesLeadOpportunity, CRMProposal,
    CRMProposalRecipient, CRMProposalSubmission, CRMSalesTractionReport
)

class ICRMSalesCampaignRepository(Protocol):
    def create(self, campaign: CRMSalesCampaign) -> CRMSalesCampaign: ...
    def get_by_id(self, campaign_id: int) -> Optional[CRMSalesCampaign]: ...
    def list_all(
        self,
        limit: int = 100,
        skip: int = 0,
        search: str = None,
        status: bool = None,
        primary_manager_user_id: int = None,
        start_date_from: str = None,
        start_date_to: str = None
    ) -> List[CRMSalesCampaign]: ...
    def list_active(self, limit: int = 20) -> List[CRMSalesCampaign]: ...
    def update(self, campaign_id: int, **kwargs) -> Optional[CRMSalesCampaign]: ...
    def delete(self, campaign_id: int) -> bool: ...

class ICRMSalesLeadRepository(Protocol):
    def create(self, lead: CRMSalesLeadOpportunity) -> CRMSalesLeadOpportunity: ...
    def get_by_id(self, lead_id: int) -> Optional[CRMSalesLeadOpportunity]: ...
    def list_all(self, limit: int = 20) -> List[CRMSalesLeadOpportunity]: ...
    def list_by_campaign(self, campaign_id: int, limit: int = 20) -> List[CRMSalesLeadOpportunity]: ...
    def list_by_status(self, status_id: int, limit: int = 20) -> List[CRMSalesLeadOpportunity]: ...
    def update(self, lead_id: int, **kwargs) -> Optional[CRMSalesLeadOpportunity]: ...
    def delete(self, lead_id: int) -> bool: ...

class ICRMProposalRepository(Protocol):
    def create(self, proposal: CRMProposal) -> CRMProposal: ...
    def get_by_id(self, proposal_id: int) -> Optional[CRMProposal]: ...
    def list_all(self, limit: int = 20) -> List[CRMProposal]: ...
    def list_by_status(self, status_id: int, limit: int = 20) -> List[CRMProposal]: ...
    def list_by_company(self, company_id: int, limit: int = 20) -> List[CRMProposal]: ...
    def update(self, proposal_id: int, **kwargs) -> Optional[CRMProposal]: ...
    def delete(self, proposal_id: int) -> bool: ...

class ICRMProposalRecipientRepository(Protocol):
    def create(self, recipient: CRMProposalRecipient) -> CRMProposalRecipient: ...
    def get_by_id(self, recipient_id: int) -> Optional[CRMProposalRecipient]: ...
    def list_by_proposal(self, proposal_id: int) -> List[CRMProposalRecipient]: ...
    def update(self, recipient_id: int, **kwargs) -> Optional[CRMProposalRecipient]: ...
    def delete(self, recipient_id: int) -> bool: ...

class ICRMProposalSubmissionRepository(Protocol):
    def create(self, submission: CRMProposalSubmission) -> CRMProposalSubmission: ...
    def get_by_id(self, submission_id: int) -> Optional[CRMProposalSubmission]: ...
    def list_by_proposal(self, proposal_id: int, limit: int = 20) -> List[CRMProposalSubmission]: ...
    def update(self, submission_id: int, **kwargs) -> Optional[CRMProposalSubmission]: ...

class CRMSalesCampaignRepository(ICRMSalesCampaignRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, campaign: CRMSalesCampaign) -> CRMSalesCampaign:
        self.db.add(campaign)
        self.db.commit()
        self.db.refresh(campaign)
        return campaign

    def get_by_id(self, campaign_id: int) -> Optional[CRMSalesCampaign]:
        return self.db.query(CRMSalesCampaign).filter(CRMSalesCampaign.id == campaign_id).first()

    def list_all(
        self,
        limit: int = 100,
        skip: int = 0,
        search: str = None,
        status: bool = None,
        primary_manager_user_id: int = None,
        start_date_from: str = None,
        start_date_to: str = None
    ) -> List[CRMSalesCampaign]:
        query = self.db.query(CRMSalesCampaign)
        
        # Apply search filter (search in name and description)
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                (CRMSalesCampaign.name.ilike(search_pattern)) |
                (CRMSalesCampaign.description.ilike(search_pattern))
            )
        
        # Apply status filter
        if status is not None:
            query = query.filter(CRMSalesCampaign.status_open_closed == status)
        
        # Apply owner filter
        if primary_manager_user_id is not None:
            query = query.filter(CRMSalesCampaign.primary_manager_user_id == primary_manager_user_id)
        
        # Apply date range filters
        if start_date_from:
            try:
                from datetime import datetime
                date_from = datetime.fromisoformat(start_date_from.replace('Z', '+00:00'))
                query = query.filter(CRMSalesCampaign.start_date >= date_from)
            except ValueError:
                pass
        
        if start_date_to:
            try:
                from datetime import datetime
                date_to = datetime.fromisoformat(start_date_to.replace('Z', '+00:00'))
                query = query.filter(CRMSalesCampaign.start_date <= date_to)
            except ValueError:
                pass
        
        # Apply ordering, pagination
        return query.order_by(CRMSalesCampaign.created_at.desc()).offset(skip).limit(limit).all()

    def list_active(self, limit: int = 20) -> List[CRMSalesCampaign]:
        return self.db.query(CRMSalesCampaign).filter(
            CRMSalesCampaign.status_open_closed == True
        ).order_by(CRMSalesCampaign.created_at.desc()).limit(limit).all()

    def update(self, campaign_id: int, **kwargs) -> Optional[CRMSalesCampaign]:
        campaign = self.get_by_id(campaign_id)
        if campaign:
            for key, value in kwargs.items():
                setattr(campaign, key, value)
            self.db.commit()
            self.db.refresh(campaign)
        return campaign

    def delete(self, campaign_id: int) -> bool:
        campaign = self.get_by_id(campaign_id)
        if campaign:
            self.db.delete(campaign)
            self.db.commit()
            return True
        return False

class CRMSalesLeadRepository(ICRMSalesLeadRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, lead: CRMSalesLeadOpportunity) -> CRMSalesLeadOpportunity:
        self.db.add(lead)
        self.db.commit()
        self.db.refresh(lead)
        return lead

    def get_by_id(self, lead_id: int) -> Optional[CRMSalesLeadOpportunity]:
        return self.db.query(CRMSalesLeadOpportunity).filter(CRMSalesLeadOpportunity.id == lead_id).first()

    def list_all(self, limit: int = 20) -> List[CRMSalesLeadOpportunity]:
        return self.db.query(CRMSalesLeadOpportunity).limit(limit).all()

    def list_by_campaign(self, campaign_id: int, limit: int = 20) -> List[CRMSalesLeadOpportunity]:
        return self.db.query(CRMSalesLeadOpportunity).filter(
            CRMSalesLeadOpportunity.crm_sales_campaign_id == campaign_id
        ).order_by(CRMSalesLeadOpportunity.created_at.desc()).limit(limit).all()

    def list_by_status(self, status_id: int, limit: int = 20) -> List[CRMSalesLeadOpportunity]:
        return self.db.query(CRMSalesLeadOpportunity).filter(
            CRMSalesLeadOpportunity.crm_sales_lead_status_id == status_id
        ).order_by(CRMSalesLeadOpportunity.created_at.desc()).limit(limit).all()

    def update(self, lead_id: int, **kwargs) -> Optional[CRMSalesLeadOpportunity]:
        lead = self.get_by_id(lead_id)
        if lead:
            for key, value in kwargs.items():
                setattr(lead, key, value)
            self.db.commit()
            self.db.refresh(lead)
        return lead

    def delete(self, lead_id: int) -> bool:
        lead = self.get_by_id(lead_id)
        if lead:
            self.db.delete(lead)
            self.db.commit()
            return True
        return False

class CRMProposalRepository(ICRMProposalRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, proposal: CRMProposal) -> CRMProposal:
        self.db.add(proposal)
        self.db.commit()
        self.db.refresh(proposal)
        return proposal

    def get_by_id(self, proposal_id: int) -> Optional[CRMProposal]:
        return self.db.query(CRMProposal).filter(CRMProposal.id == proposal_id).first()

    def list_all(self, limit: int = 20) -> List[CRMProposal]:
        return self.db.query(CRMProposal).order_by(CRMProposal.created_at.desc()).limit(limit).all()

    def list_by_status(self, status_id: int, limit: int = 20) -> List[CRMProposal]:
        return self.db.query(CRMProposal).filter(
            CRMProposal.proposal_status_id == status_id
        ).order_by(CRMProposal.created_at.desc()).limit(limit).all()

    def list_by_company(self, company_id: int, limit: int = 20) -> List[CRMProposal]:
        return self.db.query(CRMProposal).filter(
            CRMProposal.primary_company_id == company_id
        ).order_by(CRMProposal.created_at.desc()).limit(limit).all()

    def update(self, proposal_id: int, **kwargs) -> Optional[CRMProposal]:
        proposal = self.get_by_id(proposal_id)
        if proposal:
            for key, value in kwargs.items():
                setattr(proposal, key, value)
            self.db.commit()
            self.db.refresh(proposal)
        return proposal

    def delete(self, proposal_id: int) -> bool:
        proposal = self.get_by_id(proposal_id)
        if proposal:
            self.db.delete(proposal)
            self.db.commit()
            return True
        return False

class CRMProposalRecipientRepository(ICRMProposalRecipientRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, recipient: CRMProposalRecipient) -> CRMProposalRecipient:
        self.db.add(recipient)
        self.db.commit()
        self.db.refresh(recipient)
        return recipient

    def get_by_id(self, recipient_id: int) -> Optional[CRMProposalRecipient]:
        return self.db.query(CRMProposalRecipient).filter(CRMProposalRecipient.id == recipient_id).first()

    def list_by_proposal(self, proposal_id: int) -> List[CRMProposalRecipient]:
        return self.db.query(CRMProposalRecipient).filter(
            CRMProposalRecipient.proposal_id == proposal_id
        ).all()

    def update(self, recipient_id: int, **kwargs) -> Optional[CRMProposalRecipient]:
        recipient = self.get_by_id(recipient_id)
        if recipient:
            for key, value in kwargs.items():
                setattr(recipient, key, value)
            self.db.commit()
            self.db.refresh(recipient)
        return recipient

    def delete(self, recipient_id: int) -> bool:
        recipient = self.get_by_id(recipient_id)
        if recipient:
            self.db.delete(recipient)
            self.db.commit()
            return True
        return False

class CRMProposalSubmissionRepository(ICRMProposalSubmissionRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, submission: CRMProposalSubmission) -> CRMProposalSubmission:
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        return submission

    def get_by_id(self, submission_id: int) -> Optional[CRMProposalSubmission]:
        return self.db.query(CRMProposalSubmission).filter(CRMProposalSubmission.id == submission_id).first()

    def list_by_proposal(self, proposal_id: int, limit: int = 20) -> List[CRMProposalSubmission]:
        return self.db.query(CRMProposalSubmission).filter(
            CRMProposalSubmission.proposal_id == proposal_id
        ).order_by(CRMProposalSubmission.created_at.desc()).limit(limit).all()

    def update(self, submission_id: int, **kwargs) -> Optional[CRMProposalSubmission]:
        submission = self.get_by_id(submission_id)
        if submission:
            for key, value in kwargs.items():
                setattr(submission, key, value)
            self.db.commit()
            self.db.refresh(submission)
        return submission
