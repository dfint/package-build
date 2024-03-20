from pydantic import BaseModel, ConfigDict


class HookInfoEntry(BaseModel):
    df: int
    checksum: int
    lib: str
    config: str
    offsets: str
    
    model_config = ConfigDict(frozen=True)


class DictInfoEntry(BaseModel):
    language: str
    csv: str
    font: str
    encoding: str
    checksum: int

    def __str__(self):
        return self.language
    
    model_config = ConfigDict(frozen=True)
