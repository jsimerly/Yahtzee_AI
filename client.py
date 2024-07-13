from scorecard import ScoreCard
import numpy as np
from numpy.typing import NDArray
from enum import Enum
from typing import TYPE_CHECKING
from helper import np_concat

if TYPE_CHECKING:
    from models.base import YahtzeeModel
    from typing import Type

class PhaseState(Enum):
    HOLDING = 0
    SCORING = 1

class GameClient:
    def __init__(self, Model: Type[YahtzeeModel]) -> None:
        self.model = Model
        self._active = False
        self.phase_state = PhaseState.HOLDING

        self.round: int
        self.scorecard: ScoreCard
        self.rolls : int

        self.curr_state: list
        self.curr_decisions: list

        self.games_states: list
        self.game_hold_decisions: list
        self.game_score_decisions: list
        self.game_scores: list
        
        self.reset_game()

    def reset_game(self):
        self.scorecard = ScoreCard()
        self.rounds = 0
        self.rolls = 3

        self.curr_state = []
        self.curr_decisions = []

        self.games_states = []
        self.game_hold_decisions = []
        self.game_score_decisions = []
        self.game_scores = []

        self.dice = np.array([0 for _ in range(5)])
        self.holding_dice = np.array([True for _ in range(5)])


    def run(self):
        self._active = True
        self.reset_game()
 
        while self._active:
            self.start_turn()
            
    def start_turn(self):
        self._clear_turn_states()
    
        self.phase_state = PhaseState.HOLDING
        while self.rolls > 0:
            self.roll()
            self.hold_step()

        self.phase_state = PhaseState.SCORING
        self.score_step()

    def _clear_turn_states(self):
        self.curr_state = []
        self.curr_decisions = []

    def roll(self):
        self.dice[~self.holding_dice] = np.random.randint(1, 7, size=np.sum(~self.holding_dice))
        self.rolls -= 1

    def hold_step(self):
        decision_info = np_concat(
            self.turn_context_state,
            self.hold_game_state,
        )

        self.holding_dice = self.model.decide_dice_holds(decision_info)

        #TODO clean this up so that we are only using np.arrays. list are too SLOW....
        self.curr_state.append(decision_info)
        self.curr_decisions.append(self.holding_dice)

        self.games_states.append(decision_info)
        self.game_hold_decisions.append(self.holding_dice)

    def score_step(self):
        decision_info = np_concat(
            self.turn_context_state,
            self.dice
        )

        #TODO maybe only offer legal options here or build that into the model.
        score_decision = self.model.decide_scoring(decision_info)
        legal_move, turn_score = self.scorecard.add_score(score_decision, self.dice)

        if not legal_move:
            raise ValueError(f"The AI attempted to make an illegal move by selected {score_decision} with the following dice: {list(self.dice)}" )
        
        self.model.train_on_turn(
            self.curr_state, 
            self.curr_decisions, 
            decision_info, 
            score_decision, 
            turn_score
        )

        self.game_score_decisions.append(score_decision)
        self.game_scores.append(turn_score)

        self.handle_turn_end()

    def handle_turn_end(self):
        self.rolls = 3
        self.round += 1

        if self.round > 13:
            self.end_game()

    def end_game(self):
        self._active = False     

        final_score = self.scorecard.total
        self.model.train_on_game(
            self.games_states,
            self.game_hold_decisions,
            self.game_score_decisions,
            self.game_scores,
            final_score,
        ) 


    @property
    def turn_context_state(self) -> NDArray:
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

