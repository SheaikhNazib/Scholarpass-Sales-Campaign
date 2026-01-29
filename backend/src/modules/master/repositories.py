from abc import ABC, abstractmethod
from typing import Optional, List

class ICountryRepository(ABC):
    @abstractmethod
    def get_all(self) -> List: pass
    @abstractmethod
    def get_by_id(self, country_id: int) -> Optional: pass
    @abstractmethod
    def get_by_name(self, name: str) -> Optional: pass

class IStateRepository(ABC):
    @abstractmethod
    def get_by_country(self, country_id: int) -> List: pass
    @abstractmethod
    def get_by_id(self, state_id: int) -> Optional: pass

class ICityRepository(ABC):
    @abstractmethod
    def get_by_state(self, state_id: int) -> List: pass
    @abstractmethod
    def get_by_country(self, country_id: int) -> List: pass
    @abstractmethod
    def get_by_id(self, city_id: int) -> Optional: pass

class ICurrencyRepository(ABC):
    @abstractmethod
    def get_all(self) -> List: pass
    @abstractmethod
    def get_by_ticker(self, ticker: str) -> Optional: pass

class ILanguageRepository(ABC):
    @abstractmethod
    def get_all(self) -> List: pass
    @abstractmethod
    def get_by_id(self, lang_id: int) -> Optional: pass

class ITimeZoneRepository(ABC):
    @abstractmethod
    def get_all(self) -> List: pass
    @abstractmethod
    def get_default(self) -> Optional: pass
    @abstractmethod
    def get_by_name(self, name: str) -> Optional: pass

class IHubRepository(ABC):
    @abstractmethod
    def get_all(self) -> List: pass
    @abstractmethod
    def get_by_id(self, hub_id: int) -> Optional: pass
    @abstractmethod
    def get_by_country(self, country_id: int) -> List: pass
    @abstractmethod
    def get_active(self) -> List: pass

class IAIModelRepository(ABC):
    @abstractmethod
    def get_all(self) -> List: pass
    @abstractmethod
    def get_active(self) -> List: pass
    @abstractmethod
    def get_by_provider(self, provider: str) -> List: pass

class IPromptLibraryRepository(ABC):
    @abstractmethod
    def get_all(self) -> List: pass
    @abstractmethod
    def get_published(self) -> List: pass
    @abstractmethod
    def get_by_category(self, category: str) -> List: pass
    @abstractmethod
    def get_by_model(self, model_id: int) -> List: pass

class IDurationTypeRepository(ABC):
    @abstractmethod
    def get_all(self) -> List: pass
    @abstractmethod
    def get_by_id(self, duration_id: int) -> Optional: pass

class ISubscriptionTypeRepository(ABC):
    @abstractmethod
    def get_all(self) -> List: pass
    @abstractmethod
    def get_active(self) -> List: pass
    @abstractmethod
    def get_by_id(self, sub_id: int) -> Optional: pass

class ITagGroupRepository(ABC):
    @abstractmethod
    def get_all(self) -> List: pass
    @abstractmethod
    def get_by_id(self, group_id: int) -> Optional: pass

class ITagCategoryRepository(ABC):
    @abstractmethod
    def get_by_group(self, group_id: int) -> List: pass
    @abstractmethod
    def get_by_id(self, category_id: int) -> Optional: pass

class ITagRepository(ABC):
    @abstractmethod
    def get_all(self) -> List: pass
    @abstractmethod
    def get_by_category(self, category_id: int) -> List: pass
    @abstractmethod
    def get_by_group(self, group_id: int) -> List: pass
    @abstractmethod
    def search(self, query: str) -> List: pass
