import uuid

from .steps.conform import Conform
from .steps.load import Load
from .read import load_schema


def standardise(
    schema: str,
    file_path: str | None = None,
    file_name: str | None = None,
    file_content: bytes | None = None,
):
    session_id = uuid.uuid4()
    _schema = load_schema(session_id, schema)
    loader = Load(
        session_id=session_id,
        file_path=file_path,
        file_name=file_name,
        file_content=file_content,
    )
    conformer = Conform(session_id=session_id, schema=_schema)
    # TODO - normaliser, validator

    loader.run()
    conformer.run()
    return conformer.dataset.export("xlsx")
