from typing import Optional, List
from src.modules.sales.repositories import (
    CRMSalesCampaignRepository, CRMSalesLeadRepository, CRMProposalRepository,
    CRMProposalRecipientRepository, CRMProposalSubmissionRepository
)
from src.modules.sales.models import (
    CRMSalesCampaign, CRMSalesLeadOpportunity, CRMProposal,
    CRMProposalRecipient, CRMProposalSubmission
)
from src.modules.sales.schemas import (
    CRMSalesCampaignSchema, CRMSalesLeadOpportunitySchema, CRMProposalSchema,
    CRMProposalRecipientSchema, CRMProposalSubmissionSchema
)

class CRMSalesCampaignService:
    def __init__(self, repo: CRMSalesCampaignRepository):
        self.repo = repo

    def create_campaign(self, schema: CRMSalesCampaignSchema) -> CRMSalesCampaignSchema:
        campaign = CRMSalesCampaign(**schema.dict(exclude_unset=True))
        created = self.repo.create(campaign)
        return CRMSalesCampaignSchema.from_orm(created)

    def get_campaign(self, campaign_id: int) -> Optional[CRMSalesCampaignSchema]:
        campaign = self.repo.get_by_id(campaign_id)
        return CRMSalesCampaignSchema.from_orm(campaign) if campaign else None

    def list_campaigns(self, limit: int = 20) -> List[CRMSalesCampaignSchema]:
        campaigns = self.repo.list_all(limit)
        return [CRMSalesCampaignSchema.from_orm(c) for c in campaigns]

    def list_active_campaigns(self, limit: int = 20) -> List[CRMSalesCampaignSchema]:
        campaigns = self.repo.list_active(limit)
        return [CRMSalesCampaignSchema.from_orm(c) for c in campaigns]

    def update_campaign(self, campaign_id: int, schema: CRMSalesCampaignSchema) -> Optional[CRMSalesCampaignSchema]:
        updated = self.repo.update(campaign_id, **schema.dict(exclude_unset=True))
        return CRMSalesCampaignSchema.from_orm(updated) if updated else None

    def delete_campaign(self, campaign_id: int) -> bool:
        return self.repo.delete(campaign_id)

class CRMSalesLeadService:
    def __init__(self, repo: CRMSalesLeadRepository):
        self.repo = repo

    def create_lead(self, schema: CRMSalesLeadOpportunitySchema) -> CRMSalesLeadOpportunitySchema:
        lead = CRMSalesLeadOpportunity(**schema.dict(exclude_unset=True))
        created = self.repo.create(lead)
        return CRMSalesLeadOpportunitySchema.from_orm(created)

    def get_lead(self, lead_id: int) -> Optional[CRMSalesLeadOpportunitySchema]:
        lead = self.repo.get_by_id(lead_id)
        return CRMSalesLeadOpportunitySchema.from_orm(lead) if lead else None

    def list_leads(self, limit: int = 20) -> List[CRMSalesLeadOpportunitySchema]:
        leads = self.repo.list_all(limit)
        return [CRMSalesLeadOpportunitySchema.from_orm(l) for l in leads]

    def list_campaign_leads(self, campaign_id: int, limit: int = 20) -> List[CRMSalesLeadOpportunitySchema]:
        leads = self.repo.list_by_campaign(campaign_id, limit)
        return [CRMSalesLeadOpportunitySchema.from_orm(l) for l in leads]

    def list_leads_by_status(self, status_id: int, limit: int = 20) -> List[CRMSalesLeadOpportunitySchema]:
        leads = self.repo.list_by_status(status_id, limit)
        return [CRMSalesLeadOpportunitySchema.from_orm(l) for l in leads]

    def update_lead(self, lead_id: int, schema: CRMSalesLeadOpportunitySchema) -> Optional[CRMSalesLeadOpportunitySchema]:
        updated = self.repo.update(lead_id, **schema.dict(exclude_unset=True))
        return CRMSalesLeadOpportunitySchema.from_orm(updated) if updated else None

    def delete_lead(self, lead_id: int) -> bool:
        return self.repo.delete(lead_id)

class CRMProposalService:
    def __init__(self, repo: CRMProposalRepository):
        self.repo = repo

    def create_proposal(self, schema: CRMProposalSchema) -> CRMProposalSchema:
        proposal = CRMProposal(**schema.dict(exclude_unset=True))
        created = self.repo.create(proposal)
        return CRMProposalSchema.from_orm(created)

    def get_proposal(self, proposal_id: int) -> Optional[CRMProposalSchema]:
        proposal = self.repo.get_by_id(proposal_id)
        return CRMProposalSchema.from_orm(proposal) if proposal else None

    def list_proposals(self, limit: int = 20) -> List[CRMProposalSchema]:
        proposals = self.repo.list_all(limit)
        return [CRMProposalSchema.from_orm(p) for p in proposals]

    def list_proposals_by_status(self, status_id: int, limit: int = 20) -> List[CRMProposalSchema]:
        proposals = self.repo.list_by_status(status_id, limit)
        return [CRMProposalSchema.from_orm(p) for p in proposals]

    def list_company_proposals(self, company_id: int, limit: int = 20) -> List[CRMProposalSchema]:
        proposals = self.repo.list_by_company(company_id, limit)
        return [CRMProposalSchema.from_orm(p) for p in proposals]

    def update_proposal(self, proposal_id: int, schema: CRMProposalSchema) -> Optional[CRMProposalSchema]:
        updated = self.repo.update(proposal_id, **schema.dict(exclude_unset=True))
        return CRMProposalSchema.from_orm(updated) if updated else None

    def delete_proposal(self, proposal_id: int) -> bool:
        return self.repo.delete(proposal_id)

class CRMProposalRecipientService:
    def __init__(self, repo: CRMProposalRecipientRepository):
        self.repo = repo

    def add_recipient(self, schema: CRMProposalRecipientSchema) -> CRMProposalRecipientSchema:
        recipient = CRMProposalRecipient(**schema.dict(exclude_unset=True))
        created = self.repo.create(recipient)
        return CRMProposalRecipientSchema.from_orm(created)

    def get_recipient(self, recipient_id: int) -> Optional[CRMProposalRecipientSchema]:
        recipient = self.repo.get_by_id(recipient_id)
        return CRMProposalRecipientSchema.from_orm(recipient) if recipient else None

    def list_proposal_recipients(self, proposal_id: int) -> List[CRMProposalRecipientSchema]:
        recipients = self.repo.list_by_proposal(proposal_id)
        return [CRMProposalRecipientSchema.from_orm(r) for r in recipients]

    def update_recipient(self, recipient_id: int, schema: CRMProposalRecipientSchema) -> Optional[CRMProposalRecipientSchema]:
        updated = self.repo.update(recipient_id, **schema.dict(exclude_unset=True))
        return CRMProposalRecipientSchema.from_orm(updated) if updated else None

    def delete_recipient(self, recipient_id: int) -> bool:
        return self.repo.delete(recipient_id)

class CRMProposalSubmissionService:
    def __init__(self, repo: CRMProposalSubmissionRepository):
        self.repo = repo

    def create_submission(self, schema: CRMProposalSubmissionSchema) -> CRMProposalSubmissionSchema:
        submission = CRMProposalSubmission(**schema.dict(exclude_unset=True))
        created = self.repo.create(submission)
        return CRMProposalSubmissionSchema.from_orm(created)

    def get_submission(self, submission_id: int) -> Optional[CRMProposalSubmissionSchema]:
        submission = self.repo.get_by_id(submission_id)
        return CRMProposalSubmissionSchema.from_orm(submission) if submission else None

    def list_proposal_submissions(self, proposal_id: int, limit: int = 20) -> List[CRMProposalSubmissionSchema]:
        submissions = self.repo.list_by_proposal(proposal_id, limit)
        return [CRMProposalSubmissionSchema.from_orm(s) for s in submissions]

    def update_submission(self, submission_id: int, schema: CRMProposalSubmissionSchema) -> Optional[CRMProposalSubmissionSchema]:
        updated = self.repo.update(submission_id, **schema.dict(exclude_unset=True))
        return CRMProposalSubmissionSchema.from_orm(updated) if updated else None
