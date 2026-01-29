"""Alembic configuration file."""

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys
from dotenv import load_dotenv

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# this is the Alembic Config object, which provides
# the values of the [alembic] section of the .ini file
# as Python attributes of an alembic.config.Config instance.
# for the purposes of generating migrations, we'll consider those
# Python attributes as the "source of truth" about the
# desired state of the schema, not the values in the .ini
# file.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from src.infrastructure.database import Base

# Import all models to register them with Base.metadata
from src.modules.user.models import AppUser, AppRole, UserRole, UserOTP, UserSession, UserNotification
from src.modules.access.models import Permission, Menu, RoleMenuPermission, UserDevice, UserContactInfo, UserAddress, UserSubscription, UserPaymentMethod, UserPaymentHistory, UserTag, UserProfileCompletion
from src.modules.notification.models import Notification
from src.modules.master.models import Country, State, County, City, ZipCode, Currency, Language, TimeZone, HubType, Hub, AIModel, AIPromptLibrary, DurationType, AppSubscriptionType, TagGroup, TagCategory, Tag, FiscalQuarter
from src.modules.connect.models import ConnectChannel, ConnectTemplate, ConnectMessage, ConnectCall
from src.modules.tpm.models import TPMTaskStatus, TPMProjectStatus, TPMTag, TPMTaskTemplate, TPMProject, TPMProjectDocument, TPMProjectTeam, TPMProjectNote, TPMTaskEvent, TPMTaskDocument, TPMTaskTeam, TPMTaskNote, TPMTaskWorkItem, TPMAIAgentRule, TPMAIAgentConversation
from src.modules.crm.models import CRMCompanyType, CRMContactType, CRMDocumentType, CRMCompany, CRMContact, CRMCompanyTag, CRMContactTag, CRMCompanyContactMap, CRMAccountRepsTeam, CRMBankInfo, CRMDocument, CRMNote, CRMGroup, CRMGroupMember, CRMGroupMessage
from src.modules.sales.models import CRMSalesLeadSourceChannel, CRMSalesLeadStatus, CRMProposalStatus, CRMProposalType, CRMProposalTemplate, CRMSalesCampaign, CRMSalesCampaignCompany, CRMSalesCampaignContact, CRMSalesCampaignExecutionTeam, CRMSalesCampaignTodo, CRMSalesCampaignDocument, CRMSalesCampaignNote, CRMSalesLeadOpportunity, CRMSalesLeadNote, CRMSalesProjection, CRMSalesTractionReport, CRMProposal, CRMProposalRecipient, CRMProposalSubmission, CRMProposalDocument, CRMCompanyProfileAICache
from src.modules.contract.models import CRMContractType, CRMContractCommissionType, CRMContract, CRMContractTerm, CRMContractMultiplePartiesSign, CRMContractTrackerTaskReminder
from src.modules.shop.models import ShopOrderChannel, ShopOrderPaymentType, ShopOrderStatus, ShopProductCategory, ShopImageVideoLibrary, ShopStoreType, ShopStore, ShopProduct, ShopOrder, ShopOrderDetail, ShopOrderPayment, ShopShoppingCart, ShopDiscountCode, ShopProductReview, ShopOrderReturn, ShopProductInventory, ShopInventoryMovement, ShopWishlist, ShopProductVariantType, ShopProductVariantValue, ShopProductVariant, ShopShippingMethod, ShopOrderShipment, ShopProductComparison, ShopStoreHours, ShopTaxRate, ShopProductSupplier

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a SQLALCHEMY_DATABASE_URL
    set in os.environ to do some form of 'offline'
    generation.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = os.getenv("DATABASE_URL")

    context.configure(
        url=configuration["sqlalchemy.url"],
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = os.getenv("DATABASE_URL")

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            render_as_batch=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
