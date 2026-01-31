#!/usr/bin/env python3
"""
Seed data script for ScholarPASS Sales Campaign backend.
This script populates the database with initial data for sales-related entities.
"""

import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to Python path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from sqlalchemy.orm import Session
from src.infrastructure.database import SessionLocal
from src.infrastructure.security import SecurityService
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
from src.modules.crm.models import CRMCompany, CRMContact
from src.modules.shop.models import ShopProduct, ShopProductCategory
from src.modules.master.models import Currency
from src.modules.user.models import AppUser, AppRole


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


def seed_currencies(db: Session):
    """Seed currencies."""
    # Check if currencies already exist
    existing_count = db.query(Currency).count()
    if existing_count > 0:
        print(f"Currencies already seeded ({existing_count} records)")
        return
    
    currencies = [
        {"name": "US Dollar", "ticker": "USD", "icon": "$", "master_country_id": 1},
        {"name": "Euro", "ticker": "EUR", "icon": "€", "master_country_id": 2},
        {"name": "British Pound", "ticker": "GBP", "icon": "£", "master_country_id": 3},
        {"name": "Japanese Yen", "ticker": "JPY", "icon": "¥", "master_country_id": 4},
        {"name": "Canadian Dollar", "ticker": "CAD", "icon": "C$", "master_country_id": 5},
        {"name": "Australian Dollar", "ticker": "AUD", "icon": "A$", "master_country_id": 6},
        {"name": "Indian Rupee", "ticker": "INR", "icon": "₹", "master_country_id": 7},
    ]

    for currency_data in currencies:
        currency = Currency(**currency_data)
        db.add(currency)
    db.commit()
    print("Seeded currencies")


def seed_roles(db: Session):
    """Seed user roles."""
    # Check if roles already exist
    existing_count = db.query(AppRole).count()
    if existing_count > 0:
        print(f"Roles already seeded ({existing_count} records)")
        return
    
    roles = [
        {"name": "Super Admin", "description": "Full system access", "is_active": True, "display_sequence": 1},
        {"name": "Sales Manager", "description": "Manage sales operations", "is_active": True, "display_sequence": 2},
        {"name": "Sales Representative", "description": "Handle sales leads", "is_active": True, "display_sequence": 3},
        {"name": "Marketing Manager", "description": "Manage marketing campaigns", "is_active": True, "display_sequence": 4},
    ]

    for role_data in roles:
        role = AppRole(**role_data)
        db.add(role)
    db.commit()
    print("Seeded roles")


def seed_users(db: Session):
    """Seed users (Lead Owners)."""
    # Check if users already exist (skip super admin seeded users)
    existing_count = db.query(AppUser).filter(AppUser.email.like('%@scholarpass.com')).count()
    if existing_count > 0:
        print(f"Users already seeded ({existing_count} records)")
        return
    
    users = [
        {
            "username": "john.doe",
            "password_hash": SecurityService.hash_password("password123"),
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@scholarpass.com",
            "phone_number": "+1-555-0201",
            "active_or_archive": True,
            "email_confirmed": True,
            "primary_role_id": 2,  # Sales Manager
            "is_public_user_internal": False,
        },
        {
            "username": "jane.smith",
            "password_hash": SecurityService.hash_password("password123"),
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@scholarpass.com",
            "phone_number": "+1-555-0202",
            "active_or_archive": True,
            "email_confirmed": True,
            "primary_role_id": 3,  # Sales Representative
            "is_public_user_internal": False,
        },
        {
            "username": "mike.johnson",
            "password_hash": SecurityService.hash_password("password123"),
            "first_name": "Mike",
            "last_name": "Johnson",
            "email": "mike.johnson@scholarpass.com",
            "phone_number": "+1-555-0203",
            "active_or_archive": True,
            "email_confirmed": True,
            "primary_role_id": 3,  # Sales Representative
            "is_public_user_internal": False,
        },
        {
            "username": "sarah.williams",
            "password_hash": SecurityService.hash_password("password123"),
            "first_name": "Sarah",
            "last_name": "Williams",
            "email": "sarah.williams@scholarpass.com",
            "phone_number": "+1-555-0204",
            "active_or_archive": True,
            "email_confirmed": True,
            "primary_role_id": 4,  # Marketing Manager
            "is_public_user_internal": False,
        },
    ]

    for user_data in users:
        user = AppUser(**user_data)
        db.add(user)
    db.commit()
    print("Seeded users")


def seed_crm_companies(db: Session):
    """Seed CRM companies."""
    # Check if companies already exist
    existing_count = db.query(CRMCompany).count()
    if existing_count > 0:
        print(f"CRM companies already seeded ({existing_count} records)")
        return
    
    companies = [
        {
            "name": "TechCorp Solutions Inc.",
            "trade_name": "TechCorp",
            "brief_profile": "Leading technology solutions provider for educational institutions",
            "industry": "Technology",
            "number_of_employees": 250,
            "annual_revenue": 15000000.00,
            "full_address": "123 Tech Street, Silicon Valley, CA 94025",
            "city": "Silicon Valley",
            "state": "California",
            "country": "United States",
            "zip_code": "94025",
            "phone": "+1-555-1001",
            "email": "info@techcorp.com",
            "website": "https://www.techcorp.com",
            "is_verified": True,
            "is_active_or_archived": True,
        },
        {
            "name": "Global Education Partners LLC",
            "trade_name": "GEP",
            "brief_profile": "International education consulting and training services",
            "industry": "Education Services",
            "number_of_employees": 150,
            "annual_revenue": 8500000.00,
            "full_address": "456 Education Ave, Boston, MA 02101",
            "city": "Boston",
            "state": "Massachusetts",
            "country": "United States",
            "zip_code": "02101",
            "phone": "+1-555-1002",
            "email": "contact@globaledu.com",
            "website": "https://www.globaledu.com",
            "is_verified": True,
            "is_active_or_archived": True,
        },
        {
            "name": "Innovation University",
            "trade_name": "IU",
            "brief_profile": "Premier research university focused on technology and innovation",
            "industry": "Higher Education",
            "number_of_employees": 2500,
            "annual_revenue": 120000000.00,
            "full_address": "789 Campus Drive, Austin, TX 78701",
            "city": "Austin",
            "state": "Texas",
            "country": "United States",
            "zip_code": "78701",
            "phone": "+1-555-1003",
            "email": "admissions@innovationuni.edu",
            "website": "https://www.innovationuni.edu",
            "is_verified": True,
            "is_active_or_archived": True,
        },
        {
            "name": "Corporate Training Institute",
            "trade_name": "CTI",
            "brief_profile": "Professional development and corporate training specialists",
            "industry": "Training & Development",
            "number_of_employees": 85,
            "annual_revenue": 4200000.00,
            "full_address": "321 Business Blvd, Chicago, IL 60601",
            "city": "Chicago",
            "state": "Illinois",
            "country": "United States",
            "zip_code": "60601",
            "phone": "+1-555-1004",
            "email": "info@corptraining.com",
            "website": "https://www.corptraining.com",
            "is_verified": True,
            "is_active_or_archived": True,
        },
        {
            "name": "EdTech Innovations Group",
            "trade_name": "ETI Group",
            "brief_profile": "Cutting-edge educational technology and software development",
            "industry": "EdTech",
            "number_of_employees": 320,
            "annual_revenue": 22000000.00,
            "full_address": "555 Innovation Park, Seattle, WA 98101",
            "city": "Seattle",
            "state": "Washington",
            "country": "United States",
            "zip_code": "98101",
            "phone": "+1-555-1005",
            "email": "hello@edtechinnovations.com",
            "website": "https://www.edtechinnovations.com",
            "is_verified": True,
            "is_active_or_archived": True,
        },
    ]

    for company_data in companies:
        company = CRMCompany(**company_data)
        db.add(company)
    db.commit()
    print("Seeded CRM companies")


def seed_crm_contacts(db: Session):
    """Seed CRM contacts."""
    # Check if contacts already exist
    existing_count = db.query(CRMContact).count()
    if existing_count > 0:
        print(f"CRM contacts already seeded ({existing_count} records)")
        return
    
    contacts = [
        {
            "first_name": "Robert",
            "last_name": "Anderson",
            "job_title": "Chief Technology Officer",
            "company_name": "TechCorp Solutions Inc.",
            "years_of_experience": 15,
            "city": "Silicon Valley",
            "state": "California",
            "country": "United States",
            "mobile": "+1-555-2001",
            "personal_email": "robert.anderson@email.com",
            "business_email": "randerson@techcorp.com",
            "personal_email_subscribed": True,
            "is_sms_subscribed": True,
        },
        {
            "first_name": "Emily",
            "last_name": "Chen",
            "job_title": "Director of Education Programs",
            "company_name": "Global Education Partners LLC",
            "years_of_experience": 12,
            "city": "Boston",
            "state": "Massachusetts",
            "country": "United States",
            "mobile": "+1-555-2002",
            "personal_email": "emily.chen@email.com",
            "business_email": "echen@globaledu.com",
            "personal_email_subscribed": True,
            "is_whatsapp_subscribed": True,
        },
        {
            "first_name": "David",
            "last_name": "Martinez",
            "job_title": "Dean of Technology",
            "company_name": "Innovation University",
            "years_of_experience": 20,
            "city": "Austin",
            "state": "Texas",
            "country": "United States",
            "mobile": "+1-555-2003",
            "personal_email": "david.martinez@email.com",
            "business_email": "dmartinez@innovationuni.edu",
            "personal_email_subscribed": True,
        },
        {
            "first_name": "Jennifer",
            "last_name": "Taylor",
            "job_title": "VP of Training Operations",
            "company_name": "Corporate Training Institute",
            "years_of_experience": 10,
            "city": "Chicago",
            "state": "Illinois",
            "country": "United States",
            "mobile": "+1-555-2004",
            "personal_email": "jennifer.taylor@email.com",
            "business_email": "jtaylor@corptraining.com",
            "personal_email_subscribed": True,
            "is_sms_subscribed": True,
        },
        {
            "first_name": "Michael",
            "last_name": "Brown",
            "job_title": "Product Manager",
            "company_name": "EdTech Innovations Group",
            "years_of_experience": 8,
            "city": "Seattle",
            "state": "Washington",
            "country": "United States",
            "mobile": "+1-555-2005",
            "personal_email": "michael.brown@email.com",
            "business_email": "mbrown@edtechinnovations.com",
            "personal_email_subscribed": True,
            "is_whatsapp_subscribed": True,
        },
        {
            "first_name": "Lisa",
            "last_name": "Wilson",
            "job_title": "Procurement Manager",
            "company_name": "Innovation University",
            "years_of_experience": 14,
            "city": "Austin",
            "state": "Texas",
            "country": "United States",
            "mobile": "+1-555-2006",
            "personal_email": "lisa.wilson@email.com",
            "business_email": "lwilson@innovationuni.edu",
            "personal_email_subscribed": True,
        },
        {
            "first_name": "James",
            "last_name": "Thompson",
            "job_title": "Sales Director",
            "company_name": "TechCorp Solutions Inc.",
            "years_of_experience": 11,
            "city": "Silicon Valley",
            "state": "California",
            "country": "United States",
            "mobile": "+1-555-2007",
            "personal_email": "james.thompson@email.com",
            "business_email": "jthompson@techcorp.com",
            "personal_email_subscribed": True,
            "is_sms_subscribed": True,
        },
    ]

    for contact_data in contacts:
        contact = CRMContact(**contact_data)
        db.add(contact)
    db.commit()
    print("Seeded CRM contacts")


def seed_product_categories(db: Session):
    """Seed shop product categories."""
    # Check if categories already exist
    existing_count = db.query(ShopProductCategory).count()
    if existing_count > 0:
        print(f"Product categories already seeded ({existing_count} records)")
        return
    
    categories = [
        {
            "name": "Online Courses",
            "description": "Digital learning courses and programs",
            "draft_or_published": "published",
            "display_sequence": 1,
        },
        {
            "name": "Certification Programs",
            "description": "Professional certification and credential programs",
            "draft_or_published": "published",
            "display_sequence": 2,
        },
        {
            "name": "Training Materials",
            "description": "Educational resources and training materials",
            "draft_or_published": "published",
            "display_sequence": 3,
        },
        {
            "name": "Consulting Services",
            "description": "Professional consulting and advisory services",
            "draft_or_published": "published",
            "display_sequence": 4,
        },
    ]

    for category_data in categories:
        category = ShopProductCategory(**category_data)
        db.add(category)
    db.commit()
    print("Seeded product categories")


def seed_shop_products(db: Session):
    """Seed shop products."""
    # Check if products already exist
    existing_count = db.query(ShopProduct).count()
    if existing_count > 0:
        print(f"Shop products already seeded ({existing_count} records)")
        return
    
    products = [
        {
            "name": "Digital Transformation Course",
            "short_description": "Comprehensive course on digital transformation strategies",
            "description": "Learn how to lead digital transformation initiatives in educational institutions. Covers change management, technology adoption, and strategic planning.",
            "sku": "DTC-001",
            "regular_price": 499.99,
            "sale_price": 399.99,
            "discount_percentage": 20.0,
            "unit_price": 399.99,
            "stock_quantity": 100,
            "draft_or_published": "published",
            "product_or_service": False,
            "verified": True,
            "product_category_id": 1,
            "master_currency_id": 1,
        },
        {
            "name": "Leadership in Education Certificate",
            "short_description": "Professional certification program for education leaders",
            "description": "Earn your Leadership in Education certificate through our comprehensive 12-week program. Includes mentorship and networking opportunities.",
            "sku": "LEC-001",
            "regular_price": 1299.99,
            "sale_price": 1099.99,
            "discount_percentage": 15.38,
            "unit_price": 1099.99,
            "stock_quantity": 50,
            "draft_or_published": "published",
            "product_or_service": False,
            "verified": True,
            "product_category_id": 2,
            "master_currency_id": 1,
        },
        {
            "name": "EdTech Implementation Toolkit",
            "short_description": "Complete toolkit for implementing educational technology",
            "description": "Everything you need to successfully implement educational technology in your institution. Includes templates, guides, and best practices.",
            "sku": "ETK-001",
            "regular_price": 299.99,
            "sale_price": 249.99,
            "discount_percentage": 16.67,
            "unit_price": 249.99,
            "stock_quantity": 200,
            "draft_or_published": "published",
            "product_or_service": False,
            "verified": True,
            "product_category_id": 3,
            "master_currency_id": 1,
        },
        {
            "name": "Strategic Planning Consultation",
            "short_description": "One-on-one strategic planning consultation service",
            "description": "Work directly with our expert consultants to develop a comprehensive strategic plan for your educational institution. Includes 10 hours of consultation.",
            "sku": "SPC-001",
            "regular_price": 2500.00,
            "sale_price": 2500.00,
            "call_for_price": False,
            "unit_price": 2500.00,
            "stock_quantity": 20,
            "draft_or_published": "published",
            "product_or_service": True,
            "verified": True,
            "product_category_id": 4,
            "master_currency_id": 1,
        },
        {
            "name": "Data Analytics for Educators",
            "short_description": "Learn to leverage data analytics in education",
            "description": "Master the fundamentals of data analytics and learn how to apply them to improve student outcomes and institutional performance.",
            "sku": "DAE-001",
            "regular_price": 599.99,
            "sale_price": 499.99,
            "discount_percentage": 16.67,
            "unit_price": 499.99,
            "stock_quantity": 150,
            "draft_or_published": "published",
            "product_or_service": False,
            "verified": True,
            "product_category_id": 1,
            "master_currency_id": 1,
        },
        {
            "name": "Instructional Design Fundamentals",
            "short_description": "Essential course for instructional designers",
            "description": "Learn the core principles of instructional design and how to create engaging, effective learning experiences.",
            "sku": "IDF-001",
            "regular_price": 449.99,
            "sale_price": 349.99,
            "discount_percentage": 22.22,
            "unit_price": 349.99,
            "stock_quantity": 120,
            "draft_or_published": "published",
            "product_or_service": False,
            "verified": True,
            "product_category_id": 1,
            "master_currency_id": 1,
        },
        {
            "name": "Change Management Workshop",
            "short_description": "Interactive workshop on managing organizational change",
            "description": "2-day intensive workshop on leading and managing change in educational organizations. Includes case studies and practical exercises.",
            "sku": "CMW-001",
            "regular_price": 899.99,
            "sale_price": 799.99,
            "discount_percentage": 11.11,
            "unit_price": 799.99,
            "stock_quantity": 30,
            "draft_or_published": "published",
            "product_or_service": True,
            "verified": True,
            "product_category_id": 4,
            "master_currency_id": 1,
        },
        {
            "name": "Student Success Strategies Program",
            "short_description": "Comprehensive program for improving student outcomes",
            "description": "Learn proven strategies and interventions to improve student retention, engagement, and success rates.",
            "sku": "SSS-001",
            "regular_price": 699.99,
            "sale_price": 599.99,
            "discount_percentage": 14.29,
            "unit_price": 599.99,
            "stock_quantity": 80,
            "draft_or_published": "published",
            "product_or_service": False,
            "verified": True,
            "product_category_id": 2,
            "master_currency_id": 1,
        },
    ]

    for product_data in products:
        product = ShopProduct(**product_data)
        db.add(product)
    db.commit()
    print("Seeded shop products")


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
            "primary_manager_user_id": None,
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
            "primary_manager_user_id": None,
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
            "lead_owner_user_id": None,
            "user_id": None,
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
            "lead_owner_user_id": None,
            "user_id": None,
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
            "lead_owner_user_id": None,
            "user_id": None,
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
            "owner_user_id": None,
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
            "owner_user_id": None,
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
            "created_by_user_id": None,
        },
        {
            "proposal_id": 1,
            "recipient_id": 2,
            "channel_type": "email",
            "submitted_at": datetime(2026, 1, 30),
            "status": "submitted",
            "response_status": "pending",
            "created_by_user_id": None,
        },
        {
            "proposal_id": 2,
            "recipient_id": 3,
            "channel_type": "email",
            "submitted_at": datetime(2026, 2, 1),
            "status": "submitted",
            "response_status": "under_review",
            "response_date": datetime(2026, 2, 5),
            "created_by_user_id": None,
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
        seed_currencies(db)
        seed_roles(db)
        seed_users(db)
        seed_lead_statuses(db)
        seed_proposal_statuses(db)
        seed_proposal_types(db)
        seed_lead_source_channels(db)
        seed_proposal_templates(db)

        # Seed CRM data
        seed_crm_companies(db)
        seed_crm_contacts(db)

        # Seed shop data
        seed_product_categories(db)
        seed_shop_products(db)

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