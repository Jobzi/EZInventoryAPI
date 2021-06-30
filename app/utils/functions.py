from typing import Union, Iterable


def filter_dict_keys(dict_in: dict, filter_keys: Union[set, Iterable], prune_null: bool = False) -> dict:
    filter_keys = filter_keys if isinstance(filter_keys, set) else set(filter_keys)
    return {key: value for key, value in dict_in.items() if key not in filter_keys and (value if prune_null else True)}


def build_from_key_value_arrays(keys: list, values: list) -> dict:
    return dict(zip(keys, values))
