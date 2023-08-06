from typing import Mapping, Iterator, Dict, TypeVar

T = TypeVar('T')
A = TypeVar('A')
B = TypeVar('B')


class ProxyDict(Mapping):
    def __iter__(self) -> Iterator:
        return iter(())

    def __len__(self) -> int:
        # return float('inf')  # Just kidding!
        return 0

    def __getitem__(self, key):
        return key


def dict_get_default(d: Dict[str, T], key: str, value: T) -> T:
    if key in d:
        return d[key]
    else:
        d[key] = value
        return value


def reverse_dict(d: Mapping) -> Mapping:
    return {value: key for key, value in d.items()}


def dict_get_reversed(d: Mapping, key: str) -> str:
    if isinstance(d, dict):
        # It's not possible to assign custom attributes to builtin objects :(
        # if not hasattr(d, '__reversed_dict'):
        #     d.__reversed_dict = reverse_dict(d)
        return reverse_dict(d)[key]
    elif isinstance(d, ProxyDict):
        return key
    else:
        raise ValueError(f'Unknown lang_mapper type: {d}')


def dict_reversed(d: Mapping[A, B]) -> Mapping[B, A]:
    if isinstance(d, Mapping):
        # It's not possible to assign custom attributes to builtin objects :(
        # if not hasattr(d, '__reversed_dict'):
        #     d.__reversed_dict = reverse_dict(d)
        return reverse_dict(d)
    elif isinstance(d, ProxyDict):
        return d
    else:
        raise ValueError(f'Unknown lang_mapper type: {d}')
