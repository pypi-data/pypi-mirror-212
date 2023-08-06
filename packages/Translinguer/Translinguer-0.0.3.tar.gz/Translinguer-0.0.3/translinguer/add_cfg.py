from typing import TYPE_CHECKING, Any, Union
import os
import codecs

from .base import TranslinguerBase, LangRenamer, FlexibleRenamer, PageFilter, Page, Section
from .utils import dict_reversed

if TYPE_CHECKING:
    SELF = Union[TranslinguerBase, 'TranslinguerCfg']
else:
    SELF = Any


class TranslinguerCfg:
    def save_cfg_by_language_page(
            self: SELF,
            output_path: str,
            lang_mapper: FlexibleRenamer = None,
            page_filter: PageFilter = None,
    ):
        # Sections from embedded sections
        print('-- Saving to CFG files...')
        lang_mapper = self._get_lang_mapper(lang_mapper)

        done_pages = 0
        for page_name, page in self.pages.items():
            languages = page.languages or self.languages
            for lng in languages:
                lines = []
                if page_filter and page_name not in page_filter:
                    continue
                for section_name, section in page.sections.items():
                    if len(section_name) > 0:
                        lines.append(f'\n[{section_name}]')
                    for key, entry in section.entries.items():
                        lines.append(f'{key}={entry.by_language[lng]}')
                fname = os.path.join(
                    output_path,
                    f'{lang_mapper[lng]}/{page_name}.cfg'
                )
                with codecs.open(fname, 'w', encoding='utf8') as file:
                    file.write('\n'.join(lines))
                done_pages += 1
            print(f'- Done page {page_name}')
        if done_pages == 0:
            raise ValueError('Nothing is written')

    def _parse_cfg(self: SELF, page_name: str, lng: str, data: str):
        result = 0
        page: Page = self.get_page(page_name)
        section: Section = page.get_section('')

        lines = data.split('\n')
        for ln in lines:
            ln = ln.strip()
            if ln.startswith('#'):
                continue
            if ln.startswith('['):
                ln = ln[1:-1]
                ln = ln.strip()
                section = page.get_section(ln)
                continue
            eq = ln.find('=')
            if eq > 0:
                key = ln[:eq]
                key = key.strip()
                value = ln[eq + 1:]
                value = value.strip()
                entry = section.get_entry(key)
                entry.by_language[lng] = value
                result += 1
        return result

    def load_cfg(self: SELF, input_path: str, lang_mapper: FlexibleRenamer = None) -> SELF:
        print('-- Parsing CFG files...')
        lang_mapper = dict_reversed(self._get_lang_mapper(lang_mapper))
        result = 0
        self.pages = {}
        add_languages = len(self.languages) == 0
        for root, dirs, files in os.walk(input_path):
            for fl in files:
                if not fl.endswith('.cfg'):
                    continue
                with codecs.open(
                    os.path.join(root, fl), 'r', encoding='utf8'
                ) as file:
                    lng = lang_mapper[os.path.split(root)[-1]]
                    if add_languages:
                        self.languages.append(lng)
                    elif lng not in self.languages:
                        raise ValueError(f'Unexpected language {lng}')
                    added = self._parse_cfg(fl[:-4], lng, file.read())
                    result += added
                    print(f'- {lng} done: {added}')

        self._set_update('Parsed CFG')
        print('- Loaded', result, 'entries')
        return self
