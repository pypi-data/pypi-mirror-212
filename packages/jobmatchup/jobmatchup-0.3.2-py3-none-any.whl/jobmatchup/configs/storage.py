from dataclasses import dataclass, field
from pathlib import Path
from typing import LiteralString

from jobmatchup.entity.db import FileConfig


__all__ = ["DBConfig"]


@dataclass
class DBConfig:
    file_path: LiteralString | Path = "vacancies.json"

    file: FileConfig = field(init=False)

    def __post_init__(self):
        self._load_file_cfg()

    def _load_file_cfg(self):
        self.file = FileConfig(file_path=self.file_path)
