from scorecard import ScoreCard
import numpy as np
from numpy.typing import NDArray
from enum import Enum
from typing import TYPE_CHECKING
from helper import np_concat

if TYPE_CHECKING:
    from models.base import YahtzeeModel
    from typing import Any

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

        self.turn_actions: NDArray = np.array()
        self.turn_context: NDArray = np.array()

        self.dice = np.array([0 for _ in range(5)])
        self.holding_dice = np.array([True for _ in range(5)])

    @property
    def turn_game_state(self) -> NDArray:
        return np_concat(
            self.rounds,                # round[1]
            self.scorecard.points,      # scorcard [13]
            self.scorecard.available    # available [13]
        )
    
    @property
    def hold_game_state(self) -> NDArray:
        return np_concat(
            self.rolls,                 # rolls left[1]
            self.dice,                  # dice[5]
            self.holding_dice,          # holding dice [5]
        )

    @property
    def score_game_state(self) -> NDArray:
        return np_concat(
            self.rounds,                # round[1]
            self.dice,                  # dice[5]
            self.scorecard.points,      # scorcard [13]
        )

    def run(self):
        self.active = True
        while self.active:
            self.start_turn()
            
    def start_turn(self):
        self.turn_actions = np.array([])
        self.turn_context = np_concat(
            self.rounds,
            self.score_game_state
        )
        while self.rolls > 0:
            self.roll()
            self.hold_step()
        self.end_turn()

    def hold_step(self):
        ai_decision = self.model.decide_dice_holds(self.hold_game_state)
        self.holding_dice = ai_decision

        self.turn_actions.append(self.hold_game_state)

        

    def score_step(self, score_selection: int) -> tuple[float, int, float]:
        ... 

    def roll(self):
        self.dice[~self.holding_dice] = np.random.randint(1, 7, size=np.sum(~self.holding_dice))
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

 

