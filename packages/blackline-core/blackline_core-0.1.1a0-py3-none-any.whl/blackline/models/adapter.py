from datetime import datetime
from typing import Any

from blackline.factories.adapter import AdapterFactory
from pydantic import BaseModel, root_validator, validator


class ConnectionConfig(BaseModel):
    ...


class AdapterConfig(BaseModel):
    type: str
    adapter: Any = None

    @validator("adapter", pre=True, always=True)
    def load_adapter_cls(cls, value, values):
        return AdapterFactory.load_adapter(name=values["type"])

    @root_validator(pre=False)
    def initialize_adapter(cls, values):
        """
        Shit design patter. The values["config"] is only added by the subclass.
        This model cannot exist on it's on and is not labeled as an ABC.
        """
        values["adapter"] = values["adapter"](values["config"])
        return values

    def deidentify(self, catalogue, start_date: datetime = datetime.now()):
        self.adapter.deidentify(catalogue=catalogue, start_date=start_date)
