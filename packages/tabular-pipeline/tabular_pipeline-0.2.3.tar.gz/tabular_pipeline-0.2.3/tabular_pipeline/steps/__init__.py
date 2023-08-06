import uuid

from tablib import Dataset

from ..read import load_step_data
from ..write import dump_step_data
from ..schemas import StepChoices


step_order = [StepChoices.LOAD, StepChoices.CONFORM, StepChoices.NORMALISE]


class StepException(Exception):
    def __init__(self, step: StepChoices | None, message: str):
        self.step = step
        self.message = message

    def __str__(self) -> str:
        return f"{self.step}: {self.message}"


class Step:
    step: StepChoices
    dataset: Dataset

    def __init__(self, session_id: uuid.UUID) -> None:
        self.session_id = session_id

    def __post_init__(self):
        if not self.step:
            raise NotImplementedError("step is not implemented")

    def run(self):
        self.read()
        self.process()
        self.dump()

    def read(self) -> None:
        if getattr(self, "dataset", None) is not None:
            return
        elif getattr(self, "step", None) is not None:
            previous_step_idx = step_order.index(self.step) - 1
            if previous_step_idx < 0:
                return
            previous_step = step_order[previous_step_idx]
            self.dataset = load_step_data(self.session_id, previous_step)

    def process(self):
        raise NotImplementedError

    def dump(self):
        dump_step_data(
            session_id=self.session_id,
            step=self.step,
            data=self.dataset.export("csv"),
        )
