import os
import uuid
from typing import Optional

import yaml
from tablib import Databook, Dataset

from . import settings
from .schemas import Schema
from .schemas import StepChoices


def load_schema(session_id: uuid.UUID, file_path: str) -> Schema:
    settings.read_logger.info(f"{session_id}: loading schema")
    with open(file_path, "rb") as fh:
        return Schema(**yaml.load(fh, Loader=yaml.FullLoader))


def load_xlsx(file_path: str) -> Dataset:
    with open(file_path, "rb") as fh:
        databook = Databook().load(fh, "xlsx")
    dataset: Dataset = databook.sheets()[
        0
    ]  # TODO - for now, one dataset is handled - it should handle many
    return dataset


def load_csv(file_path: str, delimiter: Optional[str] = ",") -> Dataset:
    with open(file_path, "r") as fh:
        # FIXME - delimiter detection is not working
        # if not delimiter:
        # delimiter = detect_csv_delimiter(fh)
        return Dataset().load(fh, format="csv", delimiter=delimiter)


def load_step_data(session_id: uuid.UUID, step: StepChoices) -> Dataset:
    step_path = os.path.join(settings.BASE_OUTPUT_DIR, str(session_id), step.value)
    file_path = os.path.join(step_path, settings.DEFAULT_STEP_FILE_NAME)
    return load_csv(file_path, delimiter=",")
