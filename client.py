from scorecard import ScoreCard
import numpy as np
from numpy.typing import NDArray
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.base import YahtzeeModel

class PhaseState(Enum):
    HOLDING = 0
    SCORING = 1

class GameClient:
    def __init__(self, model: YahtzeeModel) -> None:
        self.model = model
        self.active = False
        self.phase_state = PhaseState.HOLDING
        self.reset_game()

    def reset_game(self):
        self.scorecard = ScoreCard()
        self.rounds = 0
        self.rolls = 3

        self.dice = np.array([0 for _ in range(5)])
        self.rolling_dice = np.array([True for _ in range(5)])

    def run(self):
        self.active = True
        while self.active:
            self.start_turn()
            
    def start_turn(self):
        while self.rolls > 0:
            self.roll()
            self.get_user_dice_holds()
        self.end_turn()

    #return reward, game_over, score
    def hold_step(self, hold_arr: NDArray) -> tuple[float, int, float]:
        ...

    def score_step(self, score_selection: int) -> tuple[float, int, float]:
        ... 

    def roll(self):
        self.dice = np.where(self.rolling_dice, np.random.randint(1, 7, size=5), self.dice)
        self.rolls -= 1

    def get_user_dice_holds(self): 
        hold_arr = input()
        self.rolling_dice = hold_arr  

    def end_turn(self):
        self.get_user_scoring_choice()

        self.rolls = 3
        self.round += 1
        if self.round > 13:
            self.end_game()

    def get_user_scoring_choice(self):
        choice = int(input())
        points, updated = self.scorecard.add_score(choice)
        if not updated:
            self.get_user_scoring_choice()

        return points

    def end_game(self):
        self.active = False                  
