import os
import uuid

from .schemas import StepChoices
from .settings import BASE_OUTPUT_DIR
from .util import create_dir


def create_output_dir(session_id: uuid.UUID, path: str):
    create_dir(BASE_OUTPUT_DIR)
    output_path = create_dir(os.path.join(BASE_OUTPUT_DIR, str(session_id)))
    output_dir = os.path.join(output_path, path)
    create_dir(output_dir)
    return output_dir


def dump_step_data(session_id: uuid.UUID, step: StepChoices, data: str) -> str:
    output_dir = create_output_dir(session_id, step.value)
    output_file = os.path.join(output_dir, "dataset.csv")
    with open(output_file, "w") as f:
        f.write(data)
    return output_file
