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

    @property
    def dfhooks_name(self) -> str:
        return self.dfhooks.rpartition("/")[-1]


class DictInfoEntry(BaseConfiguredModel):
    language: str
    code: str
    csv: str
    font: str
    encoding: str
    checksum: int

    def __str__(self) -> str:
        return self.language
