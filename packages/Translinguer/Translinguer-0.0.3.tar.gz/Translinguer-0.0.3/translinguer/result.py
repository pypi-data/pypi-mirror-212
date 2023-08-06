from .base import TranslinguerBase
from .add_cache import TranslinguerCache
from .add_gsheets import TranslinguerGsheets
from .add_csv import TranslinguerCsv
from .add_ini import TranslinguerIni
from .add_cfg import TranslinguerCfg


class Translinguer(
    TranslinguerBase,
    TranslinguerCache, TranslinguerGsheets,
    TranslinguerCsv, TranslinguerIni, TranslinguerCfg,
):
    pass
