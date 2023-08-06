from typing import TYPE_CHECKING, Any, Union, Optional, List

from .base import TranslinguerBase, PageFilter, Locales, Page, Section

DEFAULT_GSHEETS_CRED_FILE = 'gsheets-credentials.json'

if TYPE_CHECKING:
    SELF = Union[TranslinguerBase, 'TranslinguerGsheets']
else:
    SELF = Any


class TranslinguerGsheets:
    def _google_auth(
            self: SELF,
            credfile: str = DEFAULT_GSHEETS_CRED_FILE,
    ):
        '''
        Provides Google Sheets auth from a credentials file
        To learn how to create such file, see the following:
        https://github.com/burnash/gspread/issues/512
        https://youtu.be/vISRn5qFrkM

        Parameters
        ----------
        credfile: str, optional
            JSON with Google Sheets credentials
            Defaults to "gsheets-credentials.json"
        '''
        from oauth2client.service_account import ServiceAccountCredentials
        import gspread

        scope = [
            'https://www.googleapis.com/auth/drive',
            'https://spreadsheets.google.com/feeds',
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            credfile, scope)
        client = gspread.authorize(creds)
        return client

    def load_from_gsheets(
            self: SELF,
            client: Optional[object] = None,
            name: Optional[str] = None,
            key: Optional[str] = None,
            page_filter: PageFilter = None,
            merge_pages: Optional[str] = None,
            comment_prefix: str = '#',
            section_prefix: str = '[',
            section_postfix: str = ']',
    ) -> SELF:
        '''
        Uses this lib:
        https://docs.gspread.org/
        https://github.com/burnash/gspread

        Parameters
        ----------
        client: gspread.Client

        name: str, optional
            Google sheet filename
        key: str, optional
            Google sheet URL key

        page_filter: set[str], optional
            Parses sheets with specified names only
        merge_pages: str, optional
            Merge sheets into one page of given name

        comment_prefix: str
            If the first column starts with this,
            the line is considered as a comment
        section_prefix: str
            If the first column starts with this,
            it is considered as a section declaration
        section_postfix: str
            Section postfix to clean its name
        '''

        print('-- Downloading from Google Sheets...')

        if client is None:
            client = self._google_auth()

        if name is not None:
            document = client.open(name)
        elif key is not None:
            document = client.open_by_key(key)
        else:
            raise ValueError('Either name or key must be given')

        worksheets = document.worksheets()
        print(str(len(worksheets)) + ' pages:')

        page: Page
        section: Section

        for sheet in worksheets:
            if page_filter and sheet.title not in page_filter:
                continue

            content = sheet.get_all_values()
            if len(content) < 2:
                continue
            header = content[0]
            content = content[1:]
            assert header[0] == 'key', header
            languages: List[str] = header[1:]
            if len(self.languages) < len(languages):
                self.languages = languages

            print(f'- Page "{sheet.title}": {len(content)} rows.')
            if merge_pages:
                page = self.get_page(merge_pages)
                section = page.get_section(sheet.title)
            else:
                page = self.get_page(sheet.title)
                section = page.get_section('')
            if len(page.languages) < len(languages):
                page.languages = languages

            for row in content:
                key = row[0].strip()
                # Ignore empty lines
                if len(key) < 1:
                    continue
                # Ignore comments
                if key.startswith(comment_prefix):
                    continue
                # Handle sections
                if key.startswith(section_prefix):
                    key = key[len(section_prefix):-len(section_postfix)]
                    section = page.get_section(key)
                    continue
                # Handle texts finally
                for i, lng in enumerate(languages):
                    entry = section.get_entry(key)
                    entry.by_language[lng] = row[i + 1]

        self._set_update(f'Google Sheets "{name}"')
        return self
