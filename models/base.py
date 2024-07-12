from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..scorecard import ScoreOptions
    from numpy.typing import NDArray

class YahtzeeModel(ABC):
    @abstractmethod
    def decide_dice_holds(self, hold_game_state: NDArray) -> NDArray:
        ...

    @abstractmethod
    def decide_scoring(self, scoring_game_state: NDArray) -> int:
        ...

    @abstractmethod
    def reward_holds(self) -> int:
        ...

    @abstractmethod
    def predict_hold_action(self, state) -> list[bool]:
        ...

    @abstractmethod
    def predict_score_action(self, state) -> ScoreOptions.value:
        ...