from tablib import Dataset

from .. import settings
from ..read import load_csv, load_xlsx
from ..steps import Step, StepException
from ..schemas import StepChoices
from ..util import is_xlsx


class Load(Step):
    """
    - load initial file
    - read multiple files (TODO)
    - read multiple sheets within each file (TODO)
    """
    step = StepChoices.LOAD

    def __init__(self, file_path: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.file_path = file_path

    def process(self) -> Dataset:
        settings.read_logger.info(f"{self.session_id}: READING")
        if is_xlsx(self.file_path):
            self.dataset = load_xlsx(self.file_path)
        elif self.file_path.endswith(".csv"):
            self.dataset = load_csv(self.file_path)
        else:
            raise StepException(
                self.step, f"not possible to load file {self.file_path}"
            )
        settings.read_logger.info(f"{self.session_id}: dataset loaded")
