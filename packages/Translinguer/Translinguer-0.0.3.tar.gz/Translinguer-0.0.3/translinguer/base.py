from typing import Union, Optional, Callable, TypedDict, Mapping, Dict, List
import datetime
from .utils import ProxyDict, dict_get_default

# Constants
UNKNOWN = '?'

# Common types
LanguageList = List[str]
# Source language name like => raw file / technical lang name
LangRenamer = Mapping[str, str]
FlexibleRenamer = Union[None, LangRenamer, Callable[[dict], dict]]
PageFilter = Optional[set[str]]


# Serialized types
EntryDict = Dict[str, str]
SectionDict = Dict[str, EntryDict]


# I'd prefer shorter version, but type hinting doesn't work this way :(
# DictPage = TypedDict('DictPage', dict(sections=Dict[str, DictSection], languages=LanguageList))
class PageDict(TypedDict):
    sections: Dict[str, SectionDict]
    languages: LanguageList


class DocumentDict(TypedDict):
    # Main data
    pages: Dict[str, PageDict]
    languages: LanguageList
    # Additional info
    last_update: str
    source: str


# Main classes

class Entry:
    key: str
    by_language: Dict[str, str]

    def __init__(self, key: str, data: EntryDict = None):
        self.key = key
        self.by_language = data if data is not None else {}

    def __len__(self):
        return len(self.by_language)

    def to_dict(self) -> EntryDict:
        return self.by_language


class Section:
    name: str
    entries: Dict[str, Entry]

    def __init__(self, name: str, data: SectionDict = None):
        self.name = name
        data = data if data is not None else {}
        self.entries = {
            key: Entry(key, deeper)
            for key, deeper in data.items()
        }

    def __len__(self):
        return len(self.entries)

    def to_dict(self) -> SectionDict:
        return {
            key: section.to_dict()
            for key, section in self.entries.items()
        }

    def get_entry(self, key: str) -> Entry:
        return dict_get_default(self.entries, key, Entry(key))


class Page:
    name: str
    sections: Dict[str, Section]
    languages: Optional[LanguageList]

    def __init__(self, name: str, data: PageDict = None):
        self.name = name
        if data is None:
            self.sections = {}
            self.languages = None
        else:
            self.sections = {
                section_name: Section(section_name, deeper)
                for section_name, deeper in data['sections'].items()
            }
            self.languages = data['languages']

    def __len__(self):
        return len(self.sections)

    def to_dict(self) -> PageDict:
        return PageDict(
            sections={
                section_name: section.to_dict()
                for section_name, section in self.sections.items()
            },
            languages=self.languages,
        )

    def get_section(self, name: str) -> Section:
        return dict_get_default(self.sections, name, Section(name))


Locales = Dict[str, Page]


class TranslinguerBase:
    # Main data
    pages: Locales
    languages: LanguageList
    # Additional info
    last_update: str
    source: str

    def __init__(
        self,
        languages: Optional[List[str]] = None,
        lang_mapper: Optional[LangRenamer] = None,
    ):
        self.pages = {}
        self.languages = languages if languages else []
        self.lang_mapper = lang_mapper if lang_mapper else ProxyDict()
        self.last_update = UNKNOWN
        self.source = UNKNOWN

    def _get_lang_mapper(self, lang_mapper: FlexibleRenamer = None) -> LangRenamer:
        if isinstance(lang_mapper, Callable):
            # Expecting smth like dict_reversed
            # Useful for parsing raw texts into editable table
            return lang_mapper(self.lang_mapper)
        elif lang_mapper is not None:
            return lang_mapper
        else:
            return self.lang_mapper

    def validate(self, raise_error=False):
        print('-- Validating texts...')
        problems = 0
        for page_name, page in self.pages.items():
            languages = page.languages or self.languages
            for section_name, section in page.sections.items():
                for key, entry in section.entries.items():
                    for lng in languages:
                        if not entry.by_language.get(lng):
                            problems += 1
                            path = ' -> '.join((page_name, section_name, key))
                            print(f'- Missing lng {lng} for {path}')
        if problems > 0 and raise_error:
            raise ValueError('Found {problems} problems')
        if problems == 0:
            print('- All right!')
        return problems

    def get_page(self, name: str) -> Page:
        return dict_get_default(self.pages, name, Page(name))

    def _set_update(self, source):
        self.last_update = str(datetime.datetime.now())
        self.source = source

    def __len__(self):
        return len(self.pages)

    @property
    def texts_number(self) -> int:
        return sum((
            len(entry.by_language)
            for page in self.pages.values()
            for section in page.sections.values()
            for entry in section.entries.values()
        ))

    @property
    def entries_number(self) -> int:
        return sum((
            len(section.entries)
            for page in self.pages.values()
            for section in page.sections.values()
        ))

    @property
    def stats(self) -> str:
        return (
            f'-- {self.entries_number} entries'
            f', {len(self.languages)} languages'
            f', pages: {", ".join(name for name in self.pages)}'
            f'\nFrom {self.source} of {self.last_update}'
        )

    def to_dict(self) -> DocumentDict:
        return DocumentDict(
            pages={
                page_name: section.to_dict()
                for page_name, section in self.pages.items()
            },
            languages=self.languages,
            last_update=self.last_update,
            source=self.source,
        )

    def __repr__(self):
        return f'Translinguer( {len(self.pages)} pages, {len(self.languages)} languages )'
