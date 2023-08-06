import io
import csv

from .base import TranslinguerBase, FlexibleRenamer, PageFilter


class TranslinguerCsv:
    def to_csv(
            self: TranslinguerBase,
            lang_mapper: FlexibleRenamer = None,
            page_filter: PageFilter = None,
            sections=False,
            section_prefix: str = '[',
            section_postfix: str = ']',
            delimiter: str = '\t',
    ) -> str:
        lang_mapper = self._get_lang_mapper(lang_mapper)
        output = io.StringIO()
        writer = csv.writer(output, delimiter=delimiter)
        header = ["key"] + [
            lang_mapper[lng] for lng in self.languages
        ]
        writer.writerow(header)
        for page_name, page in self.pages.items():
            if page_filter and page_name not in page_filter:
                continue
            languages = page.languages or self.languages
            for section_name, section in page.sections.items():
                if sections and len(section_name) > 0:
                    writer.writerow([f'{section_prefix}{section_name}{section_postfix}'])
                writer.writerows([
                    [key] + [entry.by_language.get(lng) for lng in languages]
                    for key, entry in section.entries.items()
                ])
        return output.getvalue()
