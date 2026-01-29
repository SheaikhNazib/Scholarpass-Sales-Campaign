from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.infrastructure.auth import get_current_user
from src.modules.master.adapters import (
    CountryRepository, StateRepository, CityRepository, CurrencyRepository,
    LanguageRepository, TimeZoneRepository, HubRepository, AIModelRepository,
    PromptLibraryRepository, DurationTypeRepository, SubscriptionTypeRepository,
    TagGroupRepository, TagCategoryRepository, TagRepository
)
from src.modules.master.services import (
    GeoService, LocalizationService, HubService, AIService,
    SubscriptionService, TagService
)
from src.modules.master.schemas import (
    CountryResponse, StateResponse, CityResponse, CurrencyResponse,
    LanguageResponse, TimeZoneResponse, HubResponse, AIModelResponse,
    AIPromptResponse, DurationTypeResponse, SubscriptionTypeResponse,
    TagGroupResponse, TagCategoryResponse, TagResponse, GeoFilterRequest,
    TagSearchRequest
)

router = APIRouter(prefix="/api/master", tags=["master"])

@router.get("/countries", response_model=list[CountryResponse])
def get_countries(db: Session = Depends(get_db)):
    service = GeoService(CountryRepository(db), StateRepository(db), CityRepository(db))
    return service.get_all_countries()

@router.get("/countries/{country_id}", response_model=CountryResponse)
def get_country(country_id: int, db: Session = Depends(get_db)):
    service = GeoService(CountryRepository(db), StateRepository(db), CityRepository(db))
    country = service.get_country(country_id)
    if not country:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")
    return country

@router.get("/countries/{country_id}/states", response_model=list[StateResponse])
def get_states(country_id: int, db: Session = Depends(get_db)):
    service = GeoService(CountryRepository(db), StateRepository(db), CityRepository(db))
    return service.get_states(country_id)

@router.get("/states/{state_id}/cities", response_model=list[CityResponse])
def get_cities_by_state(state_id: int, db: Session = Depends(get_db)):
    service = GeoService(CountryRepository(db), StateRepository(db), CityRepository(db))
    return service.get_cities(state_id=state_id)

@router.get("/countries/{country_id}/cities", response_model=list[CityResponse])
def get_cities_by_country(country_id: int, db: Session = Depends(get_db)):
    service = GeoService(CountryRepository(db), StateRepository(db), CityRepository(db))
    return service.get_cities(country_id=country_id)

@router.get("/currencies", response_model=list[CurrencyResponse])
def get_currencies(db: Session = Depends(get_db)):
    service = LocalizationService(CurrencyRepository(db), LanguageRepository(db), TimeZoneRepository(db))
    return service.get_all_currencies()

@router.get("/currencies/{ticker}", response_model=CurrencyResponse)
def get_currency(ticker: str, db: Session = Depends(get_db)):
    service = LocalizationService(CurrencyRepository(db), LanguageRepository(db), TimeZoneRepository(db))
    currency = service.get_currency(ticker)
    if not currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")
    return currency

@router.get("/languages", response_model=list[LanguageResponse])
def get_languages(db: Session = Depends(get_db)):
    service = LocalizationService(CurrencyRepository(db), LanguageRepository(db), TimeZoneRepository(db))
    return service.get_all_languages()

@router.get("/timezones", response_model=list[TimeZoneResponse])
def get_timezones(db: Session = Depends(get_db)):
    service = LocalizationService(CurrencyRepository(db), LanguageRepository(db), TimeZoneRepository(db))
    return service.get_all_timezones()

@router.get("/timezones/default", response_model=TimeZoneResponse)
def get_default_timezone(db: Session = Depends(get_db)):
    service = LocalizationService(CurrencyRepository(db), LanguageRepository(db), TimeZoneRepository(db))
    tz = service.get_default_timezone()
    if not tz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Default timezone not found")
    return tz

@router.get("/hubs", response_model=list[HubResponse])
def get_hubs(db: Session = Depends(get_db)):
    service = HubService(HubRepository(db))
    return service.get_all_hubs()

@router.get("/hubs/active", response_model=list[HubResponse])
def get_active_hubs(db: Session = Depends(get_db)):
    service = HubService(HubRepository(db))
    return service.get_active_hubs()

@router.get("/hubs/{hub_id}", response_model=HubResponse)
def get_hub(hub_id: int, db: Session = Depends(get_db)):
    service = HubService(HubRepository(db))
    hub = service.get_hub(hub_id)
    if not hub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hub not found")
    return hub

@router.get("/hubs/country/{country_id}", response_model=list[HubResponse])
def get_hubs_by_country(country_id: int, db: Session = Depends(get_db)):
    service = HubService(HubRepository(db))
    return service.get_hubs_by_country(country_id)

@router.get("/ai-models", response_model=list[AIModelResponse])
def get_ai_models(db: Session = Depends(get_db)):
    service = AIService(AIModelRepository(db), PromptLibraryRepository(db))
    return service.get_all_models()

@router.get("/ai-models/active", response_model=list[AIModelResponse])
def get_active_ai_models(db: Session = Depends(get_db)):
    service = AIService(AIModelRepository(db), PromptLibraryRepository(db))
    return service.get_active_models()

@router.get("/ai-models/provider/{provider}", response_model=list[AIModelResponse])
def get_models_by_provider(provider: str, db: Session = Depends(get_db)):
    service = AIService(AIModelRepository(db), PromptLibraryRepository(db))
    return service.get_models_by_provider(provider)

@router.get("/ai-prompts", response_model=list[AIPromptResponse])
def get_ai_prompts(db: Session = Depends(get_db)):
    service = AIService(AIModelRepository(db), PromptLibraryRepository(db))
    return service.get_all_prompts()

@router.get("/ai-prompts/published", response_model=list[AIPromptResponse])
def get_published_prompts(db: Session = Depends(get_db)):
    service = AIService(AIModelRepository(db), PromptLibraryRepository(db))
    return service.get_published_prompts()

@router.get("/ai-prompts/category/{category}", response_model=list[AIPromptResponse])
def get_prompts_by_category(category: str, db: Session = Depends(get_db)):
    service = AIService(AIModelRepository(db), PromptLibraryRepository(db))
    return service.get_prompts_by_category(category)

@router.get("/ai-prompts/model/{model_id}", response_model=list[AIPromptResponse])
def get_prompts_by_model(model_id: int, db: Session = Depends(get_db)):
    service = AIService(AIModelRepository(db), PromptLibraryRepository(db))
    return service.get_prompts_by_model(model_id)

@router.get("/subscriptions", response_model=list[SubscriptionTypeResponse])
def get_subscriptions(db: Session = Depends(get_db)):
    service = SubscriptionService(DurationTypeRepository(db), SubscriptionTypeRepository(db))
    return service.get_all_subscriptions()

@router.get("/subscriptions/active", response_model=list[SubscriptionTypeResponse])
def get_active_subscriptions(db: Session = Depends(get_db)):
    service = SubscriptionService(DurationTypeRepository(db), SubscriptionTypeRepository(db))
    return service.get_active_subscriptions()

@router.get("/subscriptions/{sub_id}", response_model=SubscriptionTypeResponse)
def get_subscription(sub_id: int, db: Session = Depends(get_db)):
    service = SubscriptionService(DurationTypeRepository(db), SubscriptionTypeRepository(db))
    subscription = service.get_subscription(sub_id)
    if not subscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    return subscription

@router.get("/durations", response_model=list[DurationTypeResponse])
def get_durations(db: Session = Depends(get_db)):
    service = SubscriptionService(DurationTypeRepository(db), SubscriptionTypeRepository(db))
    return service.get_all_durations()

@router.get("/tag-groups", response_model=list[TagGroupResponse])
def get_tag_groups(db: Session = Depends(get_db)):
    service = TagService(TagGroupRepository(db), TagCategoryRepository(db), TagRepository(db))
    return service.get_all_groups()

@router.get("/tag-groups/{group_id}", response_model=TagGroupResponse)
def get_tag_group(group_id: int, db: Session = Depends(get_db)):
    service = TagService(TagGroupRepository(db), TagCategoryRepository(db), TagRepository(db))
    group = service.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag group not found")
    return group

@router.get("/tag-groups/{group_id}/categories", response_model=list[TagCategoryResponse])
def get_tag_categories(group_id: int, db: Session = Depends(get_db)):
    service = TagService(TagGroupRepository(db), TagCategoryRepository(db), TagRepository(db))
    return service.get_categories(group_id)

@router.get("/tags", response_model=list[TagResponse])
def get_tags(db: Session = Depends(get_db)):
    service = TagService(TagGroupRepository(db), TagCategoryRepository(db), TagRepository(db))
    return service.get_all_tags()

@router.get("/tags/category/{category_id}", response_model=list[TagResponse])
def get_tags_by_category(category_id: int, db: Session = Depends(get_db)):
    service = TagService(TagGroupRepository(db), TagCategoryRepository(db), TagRepository(db))
    return service.get_tags_by_category(category_id)

@router.get("/tags/group/{group_id}", response_model=list[TagResponse])
def get_tags_by_group(group_id: int, db: Session = Depends(get_db)):
    service = TagService(TagGroupRepository(db), TagCategoryRepository(db), TagRepository(db))
    return service.get_tags_by_group(group_id)

@router.post("/tags/search", response_model=list[TagResponse])
def search_tags(req: TagSearchRequest, db: Session = Depends(get_db)):
    service = TagService(TagGroupRepository(db), TagCategoryRepository(db), TagRepository(db))
    return service.search_tags(req.query)
