from __future__ import annotations

from typing import Optional


class FilesystemNode:
    size: int
    parent: FilesystemNode
    children: dict[str, FilesystemNode]

    def __init__(
        self,
        parent: FilesystemNode,
        children: Optional[dict[FilesystemNode]] = None,
        size: Optional[int] = None,
    ):
        self.parent = parent
        self.children = children or {}
        self._size = size

    @property
    def size(self):
        if self._size is None:
            self._size = (
                sum(child.size for child in self.children.values()) or 0
            )
        return self._size
