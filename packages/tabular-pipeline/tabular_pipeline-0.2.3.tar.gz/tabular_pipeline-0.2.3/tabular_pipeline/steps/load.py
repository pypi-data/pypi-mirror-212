from tablib import Dataset

from .. import settings
from ..read import load_csv, load_xlsx
from ..steps import Step, StepException
from ..schemas import StepChoices
from ..util import is_xlsx
import os


class Load(Step):
    """
    - load initial file
    - read multiple files (TODO)
    - read multiple sheets within each file (TODO)
    """

    step = StepChoices.LOAD

    def __init__(
        self,
        file_path: str | None = None,
        file_name: str | None = None,
        file_content: bytes | None = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        if not file_content and not file_path:
            raise StepException(self.step, "file_content or file_path required")
        if file_content and not file_name:
            raise StepException(self.step, "file_name required if passing file_content")
        self.file_content = file_content
        self.file_path = file_path
        if not file_name and file_path:
            self.file_name = os.path.basename(file_path)
        else:
            self.file_name = file_name

    def process(self) -> Dataset:
        settings.read_logger.info(f"{self.session_id}: READING")
        if is_xlsx(self.file_name):
            self.dataset = load_xlsx(self.file_content or self.file_path)
        elif self.file_name.endswith(".csv"):
            self.dataset = load_csv(self.file_content or self.file_path)
        else:
            raise StepException(self.step, f"not possible to load file {self.file}")
        settings.read_logger.info(f"{self.session_id}: dataset loaded")
