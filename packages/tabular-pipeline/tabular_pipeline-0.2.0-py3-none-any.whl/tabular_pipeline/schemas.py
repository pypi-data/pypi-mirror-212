from typing import Optional

from pydantic import BaseModel
from enum import Enum


class StepChoices(Enum):
    LOAD = "LOAD"
    CONFORM = "CONFORM"
    NORMALISE = "NORMALISE"


class Choice(BaseModel):
    name: str
    aliases: list


class Column(BaseModel):
    name: str
    datatype: str
    aliases: list
    choices: Optional[list[Choice]] = None


class Schema(BaseModel):
    columns: list[Column]
