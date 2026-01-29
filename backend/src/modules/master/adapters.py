from typing import Optional, List
from sqlalchemy.orm import Session
from src.modules.master.models import (
    Country, State, City, County, ZipCode, Currency, Language, TimeZone,
    HubType, Hub, AIModel, AIPromptLibrary, DurationType, AppSubscriptionType,
    TagGroup, TagCategory, Tag, FiscalQuarter
)
from src.modules.master.repositories import (
    ICountryRepository, IStateRepository, ICityRepository, ICurrencyRepository,
    ILanguageRepository, ITimeZoneRepository, IHubRepository, IAIModelRepository,
    IPromptLibraryRepository, IDurationTypeRepository, ISubscriptionTypeRepository,
    ITagGroupRepository, ITagCategoryRepository, ITagRepository
)

class CountryRepository(ICountryRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Country]:
        return self.db.query(Country).all()

    def get_by_id(self, country_id: int) -> Optional[Country]:
        return self.db.query(Country).filter(Country.id == country_id).first()

    def get_by_name(self, name: str) -> Optional[Country]:
        return self.db.query(Country).filter(Country.name == name).first()

class StateRepository(IStateRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_country(self, country_id: int) -> List[State]:
        return self.db.query(State).filter(State.master_country_id == country_id).all()

    def get_by_id(self, state_id: int) -> Optional[State]:
        return self.db.query(State).filter(State.id == state_id).first()

class CityRepository(ICityRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_state(self, state_id: int) -> List[City]:
        return self.db.query(City).filter(City.master_state_id == state_id).all()

    def get_by_country(self, country_id: int) -> List[City]:
        return self.db.query(City).filter(City.master_country_id == country_id).all()

    def get_by_id(self, city_id: int) -> Optional[City]:
        return self.db.query(City).filter(City.id == city_id).first()

class CurrencyRepository(ICurrencyRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Currency]:
        return self.db.query(Currency).all()

    def get_by_ticker(self, ticker: str) -> Optional[Currency]:
        return self.db.query(Currency).filter(Currency.ticker == ticker).first()

class LanguageRepository(ILanguageRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Language]:
        return self.db.query(Language).all()

    def get_by_id(self, lang_id: int) -> Optional[Language]:
        return self.db.query(Language).filter(Language.id == lang_id).first()

class TimeZoneRepository(ITimeZoneRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[TimeZone]:
        return self.db.query(TimeZone).all()

    def get_default(self) -> Optional[TimeZone]:
        return self.db.query(TimeZone).filter(TimeZone.is_default == True).first()

    def get_by_name(self, name: str) -> Optional[TimeZone]:
        return self.db.query(TimeZone).filter(TimeZone.timezone_name == name).first()

class HubRepository(IHubRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Hub]:
        return self.db.query(Hub).all()

    def get_by_id(self, hub_id: int) -> Optional[Hub]:
        return self.db.query(Hub).filter(Hub.id == hub_id).first()

    def get_by_country(self, country_id: int) -> List[Hub]:
        return self.db.query(Hub).filter(Hub.master_country_id == country_id).all()

    def get_active(self) -> List[Hub]:
        return self.db.query(Hub).filter(Hub.is_active_or_planning == True).all()

class AIModelRepository(IAIModelRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[AIModel]:
        return self.db.query(AIModel).all()

    def get_active(self) -> List[AIModel]:
        return self.db.query(AIModel).filter(AIModel.is_active == True).all()

    def get_by_provider(self, provider: str) -> List[AIModel]:
        return self.db.query(AIModel).filter(AIModel.provider_name == provider).all()

class PromptLibraryRepository(IPromptLibraryRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[AIPromptLibrary]:
        return self.db.query(AIPromptLibrary).all()

    def get_published(self) -> List[AIPromptLibrary]:
        return self.db.query(AIPromptLibrary).filter(AIPromptLibrary.is_published == True).all()

    def get_by_category(self, category: str) -> List[AIPromptLibrary]:
        return self.db.query(AIPromptLibrary).filter(AIPromptLibrary.category == category).all()

    def get_by_model(self, model_id: int) -> List[AIPromptLibrary]:
        return self.db.query(AIPromptLibrary).filter(
            AIPromptLibrary.recommended_ai_model_id == model_id
        ).all()

class DurationTypeRepository(IDurationTypeRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[DurationType]:
        return self.db.query(DurationType).all()

    def get_by_id(self, duration_id: int) -> Optional[DurationType]:
        return self.db.query(DurationType).filter(DurationType.id == duration_id).first()

class SubscriptionTypeRepository(ISubscriptionTypeRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[AppSubscriptionType]:
        return self.db.query(AppSubscriptionType).all()

    def get_active(self) -> List[AppSubscriptionType]:
        return self.db.query(AppSubscriptionType).filter(AppSubscriptionType.is_active == True).all()

    def get_by_id(self, sub_id: int) -> Optional[AppSubscriptionType]:
        return self.db.query(AppSubscriptionType).filter(AppSubscriptionType.id == sub_id).first()

class TagGroupRepository(ITagGroupRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[TagGroup]:
        return self.db.query(TagGroup).all()

    def get_by_id(self, group_id: int) -> Optional[TagGroup]:
        return self.db.query(TagGroup).filter(TagGroup.id == group_id).first()

class TagCategoryRepository(ITagCategoryRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_group(self, group_id: int) -> List[TagCategory]:
        return self.db.query(TagCategory).filter(TagCategory.master_tag_group_id == group_id).all()

    def get_by_id(self, category_id: int) -> Optional[TagCategory]:
        return self.db.query(TagCategory).filter(TagCategory.id == category_id).first()

class TagRepository(ITagRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Tag]:
        return self.db.query(Tag).all()

    def get_by_category(self, category_id: int) -> List[Tag]:
        return self.db.query(Tag).filter(Tag.master_tag_category_id == category_id).all()

    def get_by_group(self, group_id: int) -> List[Tag]:
        return self.db.query(Tag).filter(Tag.master_tag_group_id == group_id).all()

    def search(self, query: str) -> List[Tag]:
        return self.db.query(Tag).filter(
            Tag.name.ilike(f"%{query}%") | Tag.synonyms.ilike(f"%{query}%")
        ).all()
