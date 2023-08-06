"""
Code follows structure of

https://github.com/njvack/markdown-to-json/blob/master/markdown_to_json/markdown_to_json.py#L58

Reused with MIT license and credit to https://github.com/njvack
"""
from typing import Any, Optional, cast

from markpickle.mypy_types import MistuneTokenList, PossibleDictTypes


def parse_outermost_dict(
    token_list: list[PossibleDictTypes], level: int
) -> PossibleDictTypes:  # was dict[Optional[str], list[dict[Optional[str], Any]]]
    """
    ATX headers, e.g. # Header, ## Subheader, can be used for a single set of nested dictionaries.
    """
    candidate = recursive_part(level, cast(MistuneTokenList, token_list))

    # recursive
    if isinstance(candidate, dict):
        for token_key, token_list in candidate.items():
            candidate[token_key] = recursive_part(level + 1, cast(MistuneTokenList, token_list))

    if candidate:
        return candidate
    # no ATX dict-like structures here.
    # mypy doesn't like this, but this is really just a hack to hold a list.
    return cast(PossibleDictTypes, {None: token_list})


def recursive_part(level: int, token_list: MistuneTokenList):
    """Recursive part of processing headers"""
    candidate = {}
    key = None
    between_values: list[dict[Optional[str], Any]] = []
    # First pass, yields candidate full of keys and lists of tokens
    for item in token_list:
        if item["type"] == "newline":
            # ignore whitespace
            continue
        if item["type"] == "heading" and item["level"] == level:
            if key:
                candidate[key] = between_values
            key = "".join(_["text"] for _ in item["children"])
            between_values = []
            continue

        between_values.append(cast(dict[Optional[str], Any], item))

    # left overs
    if key and between_values:
        candidate[key] = between_values
    if not candidate:
        return between_values
    return candidate
