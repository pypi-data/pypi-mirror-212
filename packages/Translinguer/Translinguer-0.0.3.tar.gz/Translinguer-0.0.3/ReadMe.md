# Translinguer
Allows writing simple scripts to manage locale/translation files.

The core idea behind this project is:
1. Provide a powerful yet flexible, extensible tool able to support arbitrary text types/formats 💪
2. Allow writing short and easy-to-use scripts 😊
3. It's free! 💃

Here is the simplest usage example:
```py
from translinguer import Translinguer
document = Translinguer().load_from_gsheets(name="My Translations")
document.save_cfg_by_language_page("__path__")
```

# Origin
As a startuper and indi game developer, I created lots of apps with multiple languages support,
constantly met a problem of platform/os/framework specific text files formats and a need of manual dealing with then
(which is especially painful for [cross-platform games support like TacticToy](https://www.aivanf.com/en/tactictoy)).
I found no universal tool that fits all my requirements (excepting paid services),
so I wrote separate scripts before I finally got enough (pain and) experience, understanding
to create a comprehensive tool like Translinguer.

Originally developed for [the Destiny Garden game](https://www.aivanf.com/en/destiny-garden-1)
and widely enhanced while developing [Factorio mods](https://mods.factorio.com/user/AivanF),
now I hope it can benefit other developers on various platforms!


# Workflow
My typical translating process consists of these steps:

- (Optionally) import existing raw locale files (json, ini, cfg, csv) and upload to Google Sheets
- Write/update texts in a Google Sheet (with myself, friends and volunteers, or Google Translate and ChatGPT)
- Download and parse texts from the Google Sheet
- (Optionally) Save into local cache
- Export texts to a required format (json, ini, cfg, csv)

But you may have a really different process, and Translinguer will still suit your needs!


# Inner data structure
I'm a big fan on typing and robust decomposition!
To support all the needs I met, I designed 5-layer structure:
(1) a document consists of (2) pages that consist of (3) sections
which consist of (4) entries that consist of (5) texts by language.

#### 1. Translinguer aka Document
- languages: `LanguageList = List[str]`
- texts: `Locales = Dict[PageName: str, Page]`

#### 2. Page
- name: `str`
- sections: `Dict[SectionName: str, Section]`
- languages: `Optional[LanguageList]`

#### 3. Section
- name: `str` – may be an empty string
- entries: `Dict[key: str, Entry]`

#### 4. Entry
- key: `str`
- by_language: `Dict[Language: str, text: str]`


# Usage

## 1. Simple yet verbose example

Most of the translation file formats support sections and comments.
Translinguer allows this even for tables like CSV, Google Sheets.

Consider the following table:

| key                  | Eng                           | Rus                 |
|----------------------|-------------------------------|---------------------|
| _# This is_          | _a comment_                   |                     |
| greeting             | Hello, world!                 | Привет, мир!        |
| farewell             | Good bye!                     | Всего хорошего!     |
| **\[some-section\]** |                               |                     |
| j1.1                 | In the beginning was the word | В начале было слово |

Let it be a sheet named "my-texts" in a Google Sheets document.
After parsing, it will become a Translinguer document with internal structure looking like this:
```py
{
    "languages": ["Eng", "Rus"],
    "pages": {
        "my-texts": {
           "languages": ["Eng", "Rus"],
            "sections": {
               "": {  # Default nameless section
                  "entries": {
                     "greeting": {
                        "Eng": "Hello, world!",
                        "Rus": "Привет, мир!",
                     },
                     "farewell": {
                        "Eng": "Good bye!",
                        "Rus": "Всего хорошего!",
                     },
                  }
               },
               "some-section": {
                  "entries": {
                     "j1.1": {
                        "Eng": "In the beginning was the word",
                        "Rus": "В начале было слово",
                     },
                  }
               },
            }
        }
    },
}
```

On converting to CFG files, it will become `/en/my-texts.cfg`:
```
greeting=Hello, world!
farewell=Good bye!
[some-section]
j1.1=In the beginning was the word
```
And `/ru/my-texts.cfg`:
```
greeting=Привет, мир!
farewell=Всего хорошего!
[some-section]
j1.1=В начале было слово
```

Comments and sections syntax can be easily change with methods arguments.

Notice that only a whole row may be specified as a comment, you shouldn't use it elsewhere;
btw, Google Sheets provide notes and comments which aren't content of the table, I recommend utilise it.

Here is a small script performing all these things:

```py
from translinguer import Translinguer
document = Translinguer(lang_mapper={
    'Eng': 'en',
    'Rus': 'ru',
})
document.load_from_gsheets(key="__XYZ__")
print(document.stats)
document.validate(raise_error=True)
document.save_cfg_by_language_page("__output_folder__")
```

The `lang_mapper` argument isn't required, but allows having different language names in source tables
and raw/result files, which is more readable and just fancy! ✨

The majority of methods print logs to stdout for a user to know what's going on.

## 2. Real example
Here is usage for one of my open source Factorio mods:
- [Python code](https://github.com/AivanF/factorio-Mining-Drones-Remastered/blob/main/scripts/locales.py)
- [Google Sheet texts](https://docs.google.com/spreadsheets/d/11H5p7jTiUQckTrTv250iNWP41sX4aKNjZMAzm3t_UcI/edit)

## 3. Multi-project setup
You can work with multiple projects in a single document on separate pages with different languages.
This may be useful for several small or related sets of texts so that translators can work on them in one place.

TODO: add an example...

## 4.  Customisation
You can easily customise or extend Translinguer with:
- New formats for reading/writing – just have a look at the source code.
- Your own validation logic, similarly to embedded `validate` method. Example use cases:
  - To check that all entries from your source code are present.
    You can see it in the real example mentioned above.
  - To ensure some project-specific consistency


# Install
Already wanna try it out? 😁
```bash
pip install Translinguer
# If you also wanna use Google Sheets:
pip install gspread
```


# Docs
Here is a specification of Translinguer class 🧩

### Properties
- `pages: [page_name: str, Page]` – main data storage
- `entries_number: int` – returns total number of entries
- `texts_number: int` – returns total number of texts in entries
- `stats: str` – returns a detailed string to print

### General methods

### `__init__`
- `languages: List[str], optional` – generally there is no need to set this manually
- `lang_mapper: LangRenamer = Dict[str, str], optional` – allows
  to have different language names in source tables and raw/result files.
  Defaults to `ProxyDict` which stores nothing and simply returns given key as a value.

### `validate -> int`
Checks each entry looking missing language texts. Returns number of errors, optionally raises exception.
- `raise_error: bool = False`

## Text formats

### 0. Cache (JSON)
Used to store fully serialized document data.
Filename can be specified with an argument, defaults to `DEFAULT_CACHE_FILE = 'texts.json'`

### `to_dict -> DocumentDict = Dict[str, Dict[...]]`
Converts whole document in a pure Python object.

### `from_dict`
Loads document data from a dict.
- `data: DocumentDict = Dict[str, Dict[...]]`

### `save_cache`
Saves document into `self.cache` file.
- `filename: str, optional = DEFAULT_CACHE_FILE` – cache filename

### `load_cache`
Loads document from `self.cache` file.
- `filename: str, optional = DEFAULT_CACHE_FILE` – cache filename

### 1. GSh (Google Sheets)
### `load_from_gsheets`
Updates current document with texts from specified Google Sheet table.
Sections and comments are supported, their syntax can be configured with method arguments.
Note that either `name` or `key` must be provided.

- `name: str, optional` – Google sheet filename
- `key: str, optional` – Google sheet URL key
- `page_filter: set[str], optional` – Parses sheets with specified names only
- `merge_pages: str, optional` – Merge sheets into one page of given name
- `comment_prefix: str = '#''` – If the first column starts with this, the line is considered as a comment
- `section_prefix: str = '['` – If the first column starts with this, it is considered as a section declaration
- `section_postfix: str = ']'` – Section postfix to clean its name

#### 2. CSV
### `to_csv -> str`
Exports document (whole or partially) to a CSV string.
It is useful for parsing raw text files to upload them into Google Sheet.
Sections are supported, their syntax can be configured with method arguments.

- `lang_mapper: FlexibleRenamer, optional`
- `page_filter: set[str], optional`
- `sections: bool = False` – If to write sections
- `section_prefix: str = '['` – If the first column starts with this, it is considered as a section declaration
- `section_postfix: str = ']'` – Section postfix to clean its name
- `delimiter: str = '\t'` – csv delimiter

#### 3. INI
### `save_ini_by_language`
The method saves texts into `{output_path}/{language}.{ext}` files. Note that pages get merged.

- `output_path: str`
- `lang_mapper: FlexibleRenamer, optional`
- `page_filter: set[str], optional`
- `ext: str = 'ini'`

#### 4. CFG
### `save_cfg_by_language_page`
The method saves texts into `{output_path}/{language}/{page_name}.cfg` files.
- `output_path: str`
- `lang_mapper: FlexibleRenamer, optional`
- `page_filter: set[str], optional`

### `load_cfg`
The method loads texts from `{input_path}/{language}/{page_name}.cfg` files.
- `input_path: str`
- `lang_mapper: FlexibleRenamer, optional`

## Other
Translinguer lib has some inner types, utility objects and functions.

Classes:
- `EntryDict`, `SectionDict`, `PageDict`, `DocumentDict` – used for serialization, inherited from `TypedDict`.
- `Entry`, `Section`, `Page` – actual content of `TranslinguerBase`.
- `ProxyDict` – stores nothing and simply returns given key as a value.

Types:
- `LangRenamer = Mapping[source: str, raw: str]` – mapping to keep different language names for raw and result files,
  used as init parameter, may be a `ProxyDict`.
- `FlexibleRenamer = Union[None, LangRenamer, Callable[[dict], dict]]` – optionally,
  the same mapping or a function to adjust it, notably `dict_reversed` – used to parse raw/result files.
- `PageFilter = Optional[set[str]]` – an alias for a set of page names to pick on texts exporting.
- `LanguageList = List[str]` – an alias for a list of language names as string.
- `Locales = Dict[page_name: str, Page]` – an alias for a dict of `Page` objects.


# ToDo List
General:
- Describe data structure
- Describe existing methods and supported formats
- Publish to PyPI

Core:
- Replace dicts in dicts with lists of dedicated classes
- Allow to have separate languages for pages
- Add unit-tests
- Add CI
- Add Google Translate / ChatGPT API usage
- Allow import multiple files with different languages (get rid of `self.pages =` outside of base init)

Formats:
- GSh: add page name mapping
- GSh: add saving
- CSV: add reading
- Export to iOS / Android locale files. With multiple mappings from key to components?


# Contributing
Feel free to make PRs! Just follow the guide below.
Also, you can [join my Discord](https://discord.gg/7QCXn35mU5) to discuss anything.

### New formats

1. Publish file type if it belongs to a popular platform or framework, no need of project-specific formats.

1. On adding new formats support, follow existing mixin classes type hinting approach
   and methods naming convention described in the next section.

1. "Private" methods should have file type in their names to avoid collisions.

1. Type-specific settings must be passed as method arguments (see `...` in the naming convention),
   not into class properties.

1. If you add tabular format, make sure to use arguments `comment_prefix, section_prefix, section_postfix`.
   Use existing GSh and CSV as a reference.
   
1. On document saving/loading (cases 2 & 3 in naming convention) print these events to the console,
   similarly to other formats methods.

You can use existing `add_TYPE.py` files as templates.

### Naming convention

This is naming and signature convention of file types public methods.

#### 1. Dealing with files as strings
- `from_TYPE...(content: str, ...)`
- `to_TYPE...(lang_mapper: FlexibleRenamer, ...) -> str`

#### 2. Dealing with files by local machine path
Typically, these deal with multiple raw/result files at once.

- `load_TYPE...(input_path: str, ...) -> self`
- `save_TYPE...(output_path: str, lang_mapper: FlexibleRenamer, ...)`

#### 3. Dealing with external resources like Google Drive
- `load_from_TYPE...(...) -> self`
- `save_to_TYPE...(..., lang_mapper: FlexibleRenamer)`
