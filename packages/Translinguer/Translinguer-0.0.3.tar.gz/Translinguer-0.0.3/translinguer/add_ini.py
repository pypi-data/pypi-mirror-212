import os
import codecs

from .base import TranslinguerBase, FlexibleRenamer, PageFilter


class TranslinguerIni:
    def save_ini_by_language(
            self: TranslinguerBase,
            output_path: str,
            lang_mapper: FlexibleRenamer = None,
            page_filter: PageFilter = None,
            ext: str = 'ini',
    ):
        # Sections from pages
        print('-- Saving to INI files...')
        lang_mapper = self._get_lang_mapper(lang_mapper)

        done_pages = 0
        for lng in self.languages:
            total_texts = 0
            done_texts = 0
            lines = []
            for page_name, page in self.pages.items():
                if page_filter and page_name not in page_filter:
                    continue
                for section_name, section in page.sections.items():
                    lines.append(f'\n[{section_name}]')
                    for key, entry in section.entries.items():
                        total_texts += 1
                        value = entry.by_language.get(lng)
                        if value is None:
                            continue
                        value = value.replace('"', '\\"')
                        lines.append(f'{key}="{value}"')
                        done_texts += 1

            fname = os.path.join(
                output_path,
                f'{lang_mapper[lng]}.{ext}'
            )
            with codecs.open(fname, 'w', encoding='utf8') as file:
                file.write('\n'.join(lines))
            done_pages += 1
            print(f'- Done language {lng}: {done_texts} / {total_texts}')
