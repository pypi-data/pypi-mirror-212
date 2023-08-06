from pydantic import BaseModel


__all__ = ["FileConfig"]


class FileConfig(BaseModel):
    file_path: str
