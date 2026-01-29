#!/usr/bin/env python3
"""
Seed data script for ScholarPASS Sales Campaign backend.
This script populates the database with initial data for sales-related entities.
"""

import sys
import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.infrastructure.database import SessionLocal
from src.modules.sales.models import (
    CRMSalesLeadSourceChannel,
    CRMSalesLeadStatus,
    CRMProposalStatus,
    CRMProposalType,
    CRMProposalTemplate,
    CRMSalesCampaign,
    CRMSalesLeadOpportunity,
    CRMProposal,
    CRMProposalRecipient,
    CRMProposalSubmission,
)


def seed_lead_statuses(db: Session):
    """Seed lead statuses."""
    statuses = [
        {"name": "New", "sequence_number": 1},
        {"name": "Contacted", "sequence_number": 2},
        {"name": "Qualified", "sequence_number": 3},
        {"name": "Proposal", "sequence_number": 4},
        {"name": "Negotiation", "sequence_number": 5},
        {"name": "Closed Won", "sequence_number": 6},
        {"name": "Closed Lost", "sequence_number": 7},
    ]

    for status_data in statuses:
        status = CRMSalesLeadStatus(**status_data)
        db.add(status)
    db.commit()
    print("Seeded lead statuses")


def seed_proposal_statuses(db: Session):
    """Seed proposal statuses."""
    statuses = [
        {"name": "Draft", "color_code": "#808080", "sequence": 1, "is_final": False},
        {"name": "Submitted", "color_code": "#FFA500", "sequence": 2, "is_final": False},
        {"name": "Under Review", "color_code": "#0000FF", "sequence": 3, "is_final": False},
        {"name": "Approved", "color_code": "#008000", "sequence": 4, "is_final": True},
        {"name": "Rejected", "color_code": "#FF0000", "sequence": 5, "is_final": True},
        {"name": "Awarded", "color_code": "#00FF00", "sequence": 6, "is_final": True},
    ]

    for status_data in statuses:
        status = CRMProposalStatus(**status_data)
        db.add(status)
    db.commit()
    print("Seeded proposal statuses")


def seed_proposal_types(db: Session):
    """Seed proposal types."""
    types = [
        {"name": "Grant Application", "description": "Applications for funding grants"},
        {"name": "Partnership Proposal", "description": "Proposals for business partnerships"},
        {"name": "Service Contract", "description": "Proposals for service agreements"},
        {"name": "Research Collaboration", "description": "Proposals for joint research projects"},
    ]

    for type_data in types:
        prop_type = CRMProposalType(**type_data)
        db.add(prop_type)
    db.commit()
    print("Seeded proposal types")


def seed_lead_source_channels(db: Session):
    """Seed lead source channels."""
    channels = [
        {"name": "Website", "lead_source_link": "https://scholarpass.com"},
        {"name": "Social Media", "lead_source_link": "https://facebook.com/scholarpass"},
        {"name": "Referral", "lead_source_link": None},
        {"name": "Email Campaign", "lead_source_link": None},
        {"name": "Conference", "lead_source_link": None},
    ]

    for channel_data in channels:
        channel = CRMSalesLeadSourceChannel(**channel_data)
        db.add(channel)
    db.commit()
    print("Seeded lead source channels")


def seed_proposal_templates(db: Session):
    """Seed proposal templates."""
    templates = [
        {
            "title": "Standard Grant Proposal",
            "instruction": "Use this template for standard grant applications",
            "proposals": "Template content here...",
            "csr_or_grants": True,
            "tags": "grant,funding,education",
            "published_or_draft": True,
        },
        {
            "title": "Partnership Agreement",
            "instruction": "Template for business partnership proposals",
            "proposals": "Partnership template content...",
            "csr_or_grants": False,
            "tags": "partnership,business",
            "published_or_draft": True,
        },
    ]

    for template_data in templates:
        template = CRMProposalTemplate(**template_data)
        db.add(template)
    db.commit()
    print("Seeded proposal templates")


def seed_campaigns(db: Session):
    """Seed sales campaigns."""
    campaigns = [
        {
            "name": "Spring 2026 Education Campaign",
            "description": "Campaign targeting educational institutions for spring semester",
            "location": "Global",
            "start_date": datetime(2026, 3, 1),
            "end_date": datetime(2026, 5, 31),
            "duration": "3 months",
            "projected_revenue": 500000.00,
            "revenue_earned": 0.00,
            "projected_sales": 50,
            "number_of_sales": 0,
            "campaign_budget": 100000.00,
            "spent_amount": 0.00,
            "status_open_closed": True,
            "primary_manager_user_id": 1,  # Assuming user exists
        },
        {
            "name": "Corporate Training Initiative",
            "description": "Targeted campaign for corporate training programs",
            "location": "North America",
            "start_date": datetime(2026, 2, 1),
            "end_date": datetime(2026, 6, 30),
            "duration": "5 months",
            "projected_revenue": 750000.00,
            "revenue_earned": 0.00,
            "projected_sales": 30,
            "number_of_sales": 0,
            "campaign_budget": 150000.00,
            "spent_amount": 0.00,
            "status_open_closed": True,
            "primary_manager_user_id": 1,
        },
    ]

    for campaign_data in campaigns:
        campaign = CRMSalesCampaign(**campaign_data)
        db.add(campaign)
    db.commit()
    print("Seeded campaigns")


def seed_leads(db: Session):
    """Seed sales leads."""
    leads = [
        {
            "title": "Dr.",
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@university.edu",
            "phone": "+1-555-0101",
            "job_title": "Dean of Education",
            "description": "Interested in educational technology solutions",
            "lead_score": 85,
            "expected_sales_amount": 50000.00,
            "expected_closing_date": datetime(2026, 4, 15),
            "created_date": datetime(2026, 1, 15),
            "crm_sales_campaign_id": 1,
            "crm_sales_lead_source_channel_id": 1,
            "crm_sales_lead_status_id": 2,  # Contacted
            "lead_owner_user_id": 1,
            "user_id": 1,
        },
        {
            "title": "Ms.",
            "first_name": "Sarah",
            "last_name": "Johnson",
            "email": "sarah.johnson@corp.com",
            "phone": "+1-555-0102",
            "job_title": "HR Director",
            "description": "Looking for corporate training programs",
            "lead_score": 90,
            "expected_sales_amount": 75000.00,
            "expected_closing_date": datetime(2026, 3, 30),
            "created_date": datetime(2026, 1, 20),
            "crm_sales_campaign_id": 2,
            "crm_sales_lead_source_channel_id": 3,  # Referral
            "crm_sales_lead_status_id": 3,  # Qualified
            "lead_owner_user_id": 1,
            "user_id": 1,
        },
        {
            "title": "Prof.",
            "first_name": "Michael",
            "last_name": "Davis",
            "email": "michael.davis@college.edu",
            "phone": "+1-555-0103",
            "job_title": "Department Chair",
            "description": "Research collaboration opportunity",
            "lead_score": 75,
            "expected_sales_amount": 30000.00,
            "expected_closing_date": datetime(2026, 5, 1),
            "created_date": datetime(2026, 1, 25),
            "crm_sales_campaign_id": 1,
            "crm_sales_lead_source_channel_id": 5,  # Conference
            "crm_sales_lead_status_id": 1,  # New
            "lead_owner_user_id": 1,
            "user_id": 1,
        },
    ]

    for lead_data in leads:
        lead = CRMSalesLeadOpportunity(**lead_data)
        db.add(lead)
    db.commit()
    print("Seeded leads")


def seed_proposals(db: Session):
    """Seed proposals."""
    proposals = [
        {
            "title": "Educational Technology Grant Proposal",
            "short_summary": "Proposal for implementing advanced educational technology solutions",
            "full_content": "Detailed proposal content for educational technology grant...",
            "amount_requested": 50000.00,
            "master_currency_id": 1,  # Assuming USD
            "proposal_status_id": 2,  # Submitted
            "proposal_type_id": 1,  # Grant Application
            "proposal_template_id": 1,
            "owner_user_id": 1,
            "expected_response_date": datetime(2026, 4, 1),
            "submission_deadline": datetime(2026, 3, 15),
            "submitted_at": datetime(2026, 1, 30),
            "tags": ["education", "technology", "grant"],
        },
        {
            "title": "Corporate Training Partnership",
            "short_summary": "Partnership proposal for comprehensive corporate training program",
            "full_content": "Detailed partnership proposal for corporate training...",
            "amount_requested": 75000.00,
            "master_currency_id": 1,
            "proposal_status_id": 3,  # Under Review
            "proposal_type_id": 2,  # Partnership Proposal
            "proposal_template_id": 2,
            "owner_user_id": 1,
            "expected_response_date": datetime(2026, 3, 15),
            "submission_deadline": datetime(2026, 2, 28),
            "submitted_at": datetime(2026, 2, 1),
            "tags": ["corporate", "training", "partnership"],
        },
    ]

    for proposal_data in proposals:
        proposal = CRMProposal(**proposal_data)
        db.add(proposal)
    db.commit()
    print("Seeded proposals")


def seed_proposal_recipients(db: Session):
    """Seed proposal recipients."""
    recipients = [
        {
            "proposal_id": 1,
            "recipient_role": "Primary Contact",
            "channel_preference": "email",
            "custom_email": "grants@university.edu",
            "notes": "University grants office",
        },
        {
            "proposal_id": 1,
            "recipient_role": "Secondary Contact",
            "channel_preference": "email",
            "custom_email": "tech@university.edu",
            "notes": "Technology department",
        },
        {
            "proposal_id": 2,
            "recipient_role": "Decision Maker",
            "channel_preference": "email",
            "custom_email": "ceo@corp.com",
            "notes": "Company CEO",
        },
    ]

    for recipient_data in recipients:
        recipient = CRMProposalRecipient(**recipient_data)
        db.add(recipient)
    db.commit()
    print("Seeded proposal recipients")


def seed_proposal_submissions(db: Session):
    """Seed proposal submissions."""
    submissions = [
        {
            "proposal_id": 1,
            "recipient_id": 1,
            "channel_type": "email",
            "submitted_at": datetime(2026, 1, 30),
            "status": "submitted",
            "response_status": "pending",
            "created_by_user_id": 1,
        },
        {
            "proposal_id": 1,
            "recipient_id": 2,
            "channel_type": "email",
            "submitted_at": datetime(2026, 1, 30),
            "status": "submitted",
            "response_status": "pending",
            "created_by_user_id": 1,
        },
        {
            "proposal_id": 2,
            "recipient_id": 3,
            "channel_type": "email",
            "submitted_at": datetime(2026, 2, 1),
            "status": "submitted",
            "response_status": "under_review",
            "response_date": datetime(2026, 2, 5),
            "created_by_user_id": 1,
        },
    ]

    for submission_data in submissions:
        submission = CRMProposalSubmission(**submission_data)
        db.add(submission)
    db.commit()
    print("Seeded proposal submissions")


def main():
    """Main seeding function."""
    print("Starting database seeding...")

    db = SessionLocal()
    try:
        # Seed master data first
        seed_lead_statuses(db)
        seed_proposal_statuses(db)
        seed_proposal_types(db)
        seed_lead_source_channels(db)
        seed_proposal_templates(db)

        # Seed main entities
        seed_campaigns(db)
        seed_leads(db)
        seed_proposals(db)
        seed_proposal_recipients(db)
        seed_proposal_submissions(db)

        print("Database seeding completed successfully!")

    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()