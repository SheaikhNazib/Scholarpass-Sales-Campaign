from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.modules.sales.services import (
    CRMSalesCampaignService, CRMSalesLeadService, CRMProposalService,
    CRMProposalRecipientService, CRMProposalSubmissionService
)
from src.modules.sales.repositories import (
    CRMSalesCampaignRepository, CRMSalesLeadRepository, CRMProposalRepository,
    CRMProposalRecipientRepository, CRMProposalSubmissionRepository
)
from src.modules.sales.schemas import (
    CRMSalesCampaignSchema, CRMSalesLeadOpportunitySchema, CRMProposalSchema,
    CRMProposalRecipientSchema, CRMProposalSubmissionSchema
)

router = APIRouter(prefix="/api/sales", tags=["sales"])

def get_campaign_service(db: Session = Depends(get_db)) -> CRMSalesCampaignService:
    return CRMSalesCampaignService(CRMSalesCampaignRepository(db))

def get_lead_service(db: Session = Depends(get_db)) -> CRMSalesLeadService:
    return CRMSalesLeadService(CRMSalesLeadRepository(db))

def get_proposal_service(db: Session = Depends(get_db)) -> CRMProposalService:
    return CRMProposalService(CRMProposalRepository(db))

def get_recipient_service(db: Session = Depends(get_db)) -> CRMProposalRecipientService:
    return CRMProposalRecipientService(CRMProposalRecipientRepository(db))

def get_submission_service(db: Session = Depends(get_db)) -> CRMProposalSubmissionService:
    return CRMProposalSubmissionService(CRMProposalSubmissionRepository(db))

@router.post("/campaigns", response_model=CRMSalesCampaignSchema, status_code=status.HTTP_201_CREATED)
def create_campaign(schema: CRMSalesCampaignSchema, service: CRMSalesCampaignService = Depends(get_campaign_service)):
    return service.create_campaign(schema)

@router.get("/campaigns/{campaign_id}", response_model=CRMSalesCampaignSchema)
def get_campaign(campaign_id: int, service: CRMSalesCampaignService = Depends(get_campaign_service)):
    campaign = service.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
    return campaign

@router.get("/campaigns", response_model=list[CRMSalesCampaignSchema])
def list_campaigns(
    limit: int = 100,
    skip: int = 0,
    search: str = None,
    status: bool = None,
    primary_manager_user_id: int = None,
    start_date_from: str = None,
    start_date_to: str = None,
    service: CRMSalesCampaignService = Depends(get_campaign_service)
):
    return service.list_campaigns(
        limit=limit,
        skip=skip,
        search=search,
        status=status,
        primary_manager_user_id=primary_manager_user_id,
        start_date_from=start_date_from,
        start_date_to=start_date_to
    )

@router.get("/campaigns/active", response_model=list[CRMSalesCampaignSchema])
def list_active_campaigns(limit: int = 20, service: CRMSalesCampaignService = Depends(get_campaign_service)):
    return service.list_active_campaigns(limit)

@router.put("/campaigns/{campaign_id}", response_model=CRMSalesCampaignSchema)
def update_campaign(campaign_id: int, schema: CRMSalesCampaignSchema, service: CRMSalesCampaignService = Depends(get_campaign_service)):
    updated = service.update_campaign(campaign_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
    return updated

@router.delete("/campaigns/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campaign(campaign_id: int, service: CRMSalesCampaignService = Depends(get_campaign_service)):
    if not service.delete_campaign(campaign_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")

@router.post("/leads", response_model=CRMSalesLeadOpportunitySchema, status_code=status.HTTP_201_CREATED)
def create_lead(schema: CRMSalesLeadOpportunitySchema, service: CRMSalesLeadService = Depends(get_lead_service)):
    return service.create_lead(schema)

@router.get("/leads/{lead_id}", response_model=CRMSalesLeadOpportunitySchema)
def get_lead(lead_id: int, service: CRMSalesLeadService = Depends(get_lead_service)):
    lead = service.get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    return lead

@router.get("/leads", response_model=list[CRMSalesLeadOpportunitySchema])
def list_leads(limit: int = 20, service: CRMSalesLeadService = Depends(get_lead_service)):
    return service.list_leads(limit)

@router.get("/leads/campaign/{campaign_id}", response_model=list[CRMSalesLeadOpportunitySchema])
def list_campaign_leads(campaign_id: int, limit: int = 20, service: CRMSalesLeadService = Depends(get_lead_service)):
    return service.list_campaign_leads(campaign_id, limit)

@router.get("/leads/status/{status_id}", response_model=list[CRMSalesLeadOpportunitySchema])
def list_leads_by_status(status_id: int, limit: int = 20, service: CRMSalesLeadService = Depends(get_lead_service)):
    return service.list_leads_by_status(status_id, limit)

@router.put("/leads/{lead_id}", response_model=CRMSalesLeadOpportunitySchema)
def update_lead(lead_id: int, schema: CRMSalesLeadOpportunitySchema, service: CRMSalesLeadService = Depends(get_lead_service)):
    updated = service.update_lead(lead_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
    return updated

@router.delete("/leads/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lead(lead_id: int, service: CRMSalesLeadService = Depends(get_lead_service)):
    if not service.delete_lead(lead_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")

@router.post("/proposals", response_model=CRMProposalSchema, status_code=status.HTTP_201_CREATED)
def create_proposal(schema: CRMProposalSchema, service: CRMProposalService = Depends(get_proposal_service)):
    return service.create_proposal(schema)

@router.get("/proposals/{proposal_id}", response_model=CRMProposalSchema)
def get_proposal(proposal_id: int, service: CRMProposalService = Depends(get_proposal_service)):
    proposal = service.get_proposal(proposal_id)
    if not proposal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found")
    return proposal

@router.get("/proposals", response_model=list[CRMProposalSchema])
def list_proposals(limit: int = 20, service: CRMProposalService = Depends(get_proposal_service)):
    return service.list_proposals(limit)

@router.get("/proposals/status/{status_id}", response_model=list[CRMProposalSchema])
def list_proposals_by_status(status_id: int, limit: int = 20, service: CRMProposalService = Depends(get_proposal_service)):
    return service.list_proposals_by_status(status_id, limit)

@router.get("/proposals/company/{company_id}", response_model=list[CRMProposalSchema])
def list_company_proposals(company_id: int, limit: int = 20, service: CRMProposalService = Depends(get_proposal_service)):
    return service.list_company_proposals(company_id, limit)

@router.put("/proposals/{proposal_id}", response_model=CRMProposalSchema)
def update_proposal(proposal_id: int, schema: CRMProposalSchema, service: CRMProposalService = Depends(get_proposal_service)):
    updated = service.update_proposal(proposal_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found")
    return updated

@router.delete("/proposals/{proposal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_proposal(proposal_id: int, service: CRMProposalService = Depends(get_proposal_service)):
    if not service.delete_proposal(proposal_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found")

@router.post("/proposals/{proposal_id}/recipients", response_model=CRMProposalRecipientSchema, status_code=status.HTTP_201_CREATED)
def add_recipient(proposal_id: int, schema: CRMProposalRecipientSchema, service: CRMProposalRecipientService = Depends(get_recipient_service)):
    schema.proposal_id = proposal_id
    return service.add_recipient(schema)

@router.get("/proposals/{proposal_id}/recipients/{recipient_id}", response_model=CRMProposalRecipientSchema)
def get_recipient(proposal_id: int, recipient_id: int, service: CRMProposalRecipientService = Depends(get_recipient_service)):
    recipient = service.get_recipient(recipient_id)
    if not recipient or recipient.proposal_id != proposal_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipient not found")
    return recipient

@router.get("/proposals/{proposal_id}/recipients", response_model=list[CRMProposalRecipientSchema])
def list_proposal_recipients(proposal_id: int, service: CRMProposalRecipientService = Depends(get_recipient_service)):
    return service.list_proposal_recipients(proposal_id)

@router.put("/proposals/{proposal_id}/recipients/{recipient_id}", response_model=CRMProposalRecipientSchema)
def update_recipient(proposal_id: int, recipient_id: int, schema: CRMProposalRecipientSchema, service: CRMProposalRecipientService = Depends(get_recipient_service)):
    updated = service.update_recipient(recipient_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipient not found")
    return updated

@router.delete("/proposals/{proposal_id}/recipients/{recipient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipient(proposal_id: int, recipient_id: int, service: CRMProposalRecipientService = Depends(get_recipient_service)):
    if not service.delete_recipient(recipient_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipient not found")

@router.post("/proposals/{proposal_id}/submissions", response_model=CRMProposalSubmissionSchema, status_code=status.HTTP_201_CREATED)
def create_submission(proposal_id: int, schema: CRMProposalSubmissionSchema, service: CRMProposalSubmissionService = Depends(get_submission_service)):
    schema.proposal_id = proposal_id
    return service.create_submission(schema)

@router.get("/proposals/{proposal_id}/submissions/{submission_id}", response_model=CRMProposalSubmissionSchema)
def get_submission(proposal_id: int, submission_id: int, service: CRMProposalSubmissionService = Depends(get_submission_service)):
    submission = service.get_submission(submission_id)
    if not submission or submission.proposal_id != proposal_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
    return submission

@router.get("/proposals/{proposal_id}/submissions", response_model=list[CRMProposalSubmissionSchema])
def list_proposal_submissions(proposal_id: int, limit: int = 20, service: CRMProposalSubmissionService = Depends(get_submission_service)):
    return service.list_proposal_submissions(proposal_id, limit)

@router.put("/proposals/{proposal_id}/submissions/{submission_id}", response_model=CRMProposalSubmissionSchema)
def update_submission(proposal_id: int, submission_id: int, schema: CRMProposalSubmissionSchema, service: CRMProposalSubmissionService = Depends(get_submission_service)):
    updated = service.update_submission(submission_id, schema)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
    return updated
