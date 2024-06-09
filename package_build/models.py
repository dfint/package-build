from pydantic import BaseModel, ConfigDict


class BaseConfiguredModel(BaseModel):
    model_config = ConfigDict(frozen=True)


class HookInfoEntry(BaseConfiguredModel):
    df: int
    checksum: int
    lib: str
    config: str
    offsets: str
    dfhooks: str


class DictInfoEntry(BaseConfiguredModel):
    language: str
    csv: str
    font: str
    encoding: str
    checksum: int

    def __str__(self):
        return self.language
