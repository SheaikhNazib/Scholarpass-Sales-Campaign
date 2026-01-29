from typing import Optional, List
from src.modules.master.adapters import (
    CountryRepository, StateRepository, CityRepository, CurrencyRepository,
    LanguageRepository, TimeZoneRepository, HubRepository, AIModelRepository,
    PromptLibraryRepository, DurationTypeRepository, SubscriptionTypeRepository,
    TagGroupRepository, TagCategoryRepository, TagRepository
)

class GeoService:
    def __init__(self, country_repo: CountryRepository, state_repo: StateRepository,
                 city_repo: CityRepository):
        self.country_repo = country_repo
        self.state_repo = state_repo
        self.city_repo = city_repo

    def get_all_countries(self) -> List:
        return self.country_repo.get_all()

    def get_country(self, country_id: int):
        return self.country_repo.get_by_id(country_id)

    def get_states(self, country_id: int) -> List:
        return self.state_repo.get_by_country(country_id)

    def get_cities(self, state_id: int = None, country_id: int = None) -> List:
        if state_id:
            return self.city_repo.get_by_state(state_id)
        return self.city_repo.get_by_country(country_id)

class LocalizationService:
    def __init__(self, currency_repo: CurrencyRepository, lang_repo: LanguageRepository,
                 tz_repo: TimeZoneRepository):
        self.currency_repo = currency_repo
        self.lang_repo = lang_repo
        self.tz_repo = tz_repo

    def get_all_currencies(self) -> List:
        return self.currency_repo.get_all()

    def get_currency(self, ticker: str):
        return self.currency_repo.get_by_ticker(ticker)

    def get_all_languages(self) -> List:
        return self.lang_repo.get_all()

    def get_all_timezones(self) -> List:
        return self.tz_repo.get_all()

    def get_default_timezone(self):
        return self.tz_repo.get_default()

class HubService:
    def __init__(self, hub_repo: HubRepository):
        self.hub_repo = hub_repo

    def get_all_hubs(self) -> List:
        return self.hub_repo.get_all()

    def get_hub(self, hub_id: int):
        return self.hub_repo.get_by_id(hub_id)

    def get_hubs_by_country(self, country_id: int) -> List:
        return self.hub_repo.get_by_country(country_id)

    def get_active_hubs(self) -> List:
        return self.hub_repo.get_active()

class AIService:
    def __init__(self, model_repo: AIModelRepository, prompt_repo: PromptLibraryRepository):
        self.model_repo = model_repo
        self.prompt_repo = prompt_repo

    def get_all_models(self) -> List:
        return self.model_repo.get_all()

    def get_active_models(self) -> List:
        return self.model_repo.get_active()

    def get_models_by_provider(self, provider: str) -> List:
        return self.model_repo.get_by_provider(provider)

    def get_all_prompts(self) -> List:
        return self.prompt_repo.get_all()

    def get_published_prompts(self) -> List:
        return self.prompt_repo.get_published()

    def get_prompts_by_category(self, category: str) -> List:
        return self.prompt_repo.get_by_category(category)

    def get_prompts_by_model(self, model_id: int) -> List:
        return self.prompt_repo.get_by_model(model_id)

class SubscriptionService:
    def __init__(self, duration_repo: DurationTypeRepository,
                 subscription_repo: SubscriptionTypeRepository):
        self.duration_repo = duration_repo
        self.subscription_repo = subscription_repo

    def get_all_durations(self) -> List:
        return self.duration_repo.get_all()

    def get_all_subscriptions(self) -> List:
        return self.subscription_repo.get_all()

    def get_active_subscriptions(self) -> List:
        return self.subscription_repo.get_active()

    def get_subscription(self, sub_id: int):
        return self.subscription_repo.get_by_id(sub_id)

class TagService:
    def __init__(self, group_repo: TagGroupRepository, category_repo: TagCategoryRepository,
                 tag_repo: TagRepository):
        self.group_repo = group_repo
        self.category_repo = category_repo
        self.tag_repo = tag_repo

    def get_all_groups(self) -> List:
        return self.group_repo.get_all()

    def get_group(self, group_id: int):
        return self.group_repo.get_by_id(group_id)

    def get_categories(self, group_id: int) -> List:
        return self.category_repo.get_by_group(group_id)

    def get_all_tags(self) -> List:
        return self.tag_repo.get_all()

    def get_tags_by_category(self, category_id: int) -> List:
        return self.tag_repo.get_by_category(category_id)

    def get_tags_by_group(self, group_id: int) -> List:
        return self.tag_repo.get_by_group(group_id)

    def search_tags(self, query: str) -> List:
        return self.tag_repo.search(query)
