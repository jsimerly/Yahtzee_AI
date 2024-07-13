from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..scorecard import ScoreOptions
    from numpy.typing import NDArray


class YahtzeeModel(ABC):
    @abstractmethod
    def decide_dice_holds(self, state: NDArray) -> NDArray:
        ...

    @abstractmethod
    def decide_scoring(self, state: NDArray) -> int:
        ...

    @abstractmethod
    def train_on_turn(self, 
        hold_states: list[NDArray],
        hold_decisions: list[NDArray],
        final_state: list[NDArray],
        score_category: int,
        turn_score: int,
    ) -> float:
        ...

    @abstractmethod
    def train_on_game(self,
        states: list[NDArray],
        hold_decisions: list[NDArray],
        score_decisions: list[NDArray],
        scores: list[int],
        final_scores: int
    ) -> float:
        ...
