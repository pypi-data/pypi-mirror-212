import uuid

from .steps.conform import Conform
from .steps.load import Load
from .read import load_schema


def standardise(file: str, schema: str):
    session_id = uuid.uuid4()
    schema = load_schema(session_id, schema)
    loader = Load(session_id=session_id, file_path=file)
    conformer = Conform(session_id=session_id, schema=schema)
    # TODO - normaliser, validator

    loader.run()
    conformer.run()
    return conformer.dataset.export('xlsx')
