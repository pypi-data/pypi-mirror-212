"""Base musical pattern."""
from __future__ import annotations

from typing import Any, List, Optional


class _BasePattern:
    def __init__(self, pattern: Optional[List[Any]] = None):
        if pattern is None:
            pattern = []
        self._pat = pattern

    def to_list(self):
        """Get the pattern as a list."""
        return self._pat

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, _BasePattern):
            return False
        for item, other_item in zip(self._pat, other._pat):
            if item != other_item:
                return False
        return True

    def __hash__(self):
        return hash(tuple(self._pat))

    def __len__(self) -> int:
        return len(self._pat)

    def __getitem__(self, key: int):
        return self._pat.__getitem__(key)
