from typing import Optional

from tablib import Dataset

from .. import settings
from ..schemas import Schema, StepChoices
from ..steps import Step
from ..util import normalise_entry


class Conform(Step):
    """
    - detect if the headers match the expected schema aliases
    - rename columns according to the schema
    - delete unwanted columns
    """

    step = StepChoices.CONFORM

    def __init__(
        self, schema: Schema, dataset: Optional[Dataset] = None, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.schema = schema
        self.dataset = dataset

    def process(self) -> Dataset:
        settings.conform_logger.info(f"{self.session_id}: CONFORMING")
        settings.conform_logger.info(
            f"{self.session_id}: input has {len(self.dataset.headers)} columns"
        )
        settings.conform_logger.info(
            f"{self.session_id} schema has {len(self.schema.columns)} columns"
        )
        headers_to_delete = []

        def validate_and_parse_header(header):
            _header = normalise_entry(header)
            for column in self.schema.columns:
                normalized_aliases = [
                    normalise_entry(c) for c in column.aliases + [column.name]
                ]
                if _header in normalized_aliases:
                    self.dataset.headers[idx] = column.name
                    return

            # when no match is found
            headers_to_delete.append(header)

        for idx, header in enumerate(self.dataset.headers):
            validate_and_parse_header(header)

        # delete unwanted headers
        for header in headers_to_delete:
            del self.dataset[header]

        settings.conform_logger.info(
            f"{self.session_id}: deleted {len(headers_to_delete)} columns"
        )
        settings.conform_logger.info(
            f"{self.session_id}: validated {len(self.dataset.headers)} columns"
        )

        return self.dataset
