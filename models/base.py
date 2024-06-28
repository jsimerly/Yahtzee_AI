from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..scorecard import ScoreOptions

class YahtzeeModel(ABC):
    @abstractmethod
    def get_model_dice_holds(self):
        ...

    @abstractmethod
    def get_model_scoring_choice(self):
        ...

    @abstractmethod
    def predict_hold_action(self, state) -> list[bool]:
        ...

    @abstractmethod
    def predict_score_action(self, state) -> ScoreOptions.value:
        ...