from typing import TYPE_CHECKING, Any, Union
import codecs
import json
from .base import TranslinguerBase, Page, DocumentDict

if TYPE_CHECKING:
    SELF = Union[TranslinguerBase, 'TranslinguerCache']
else:
    SELF = Any

DEFAULT_CACHE_FILE = 'texts.json'


class TranslinguerCache:
    def save_cache(self: SELF, filename: str = None, sort: bool = False):
        filename = filename or DEFAULT_CACHE_FILE
        with codecs.open(filename, 'w', encoding='utf8') as file:
            file.write(json.dumps(self.to_dict(), indent=4, sort_keys=sort, ensure_ascii=False))
        print('-- JSON cache saved.')

    def load_cache(self: SELF, filename: str = None) -> SELF:
        print('-- Loading from JSON cache...')
        filename = filename or DEFAULT_CACHE_FILE
        with codecs.open(filename, 'r', encoding='utf8') as file:
            data: DocumentDict = json.loads(file.read())
            self.from_dict(data)
        return self

    def from_dict(self: SELF, data: DocumentDict):
        self.source = data['source']
        self.last_update = data['last_update']
        self.languages = data['languages']
        self.pages = {
            page_name: Page(page_name, page)
            for page_name, page in data['pages'].items()
        }
