from pydantic import BaseModel


class HookInfoEntry(BaseModel):
    df: int
    checksum: int
    lib: str
    config: str
    offsets: str


class DictInfoEntry(BaseModel):
    language: str
    csv: str
    font: str
    encoding: str
    checksum: int

    def __str__(self):
        return self.language
