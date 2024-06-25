from scorecard import ScoreCard
import numpy as np

class GameClient:
    def __init__(self, id: int) -> None:
        self.id = id
        self.scorecard = ScoreCard()
        self.round = 1

        self.rolls = 0
        self.dice = np.array([0 for _ in range(5)])
        self.rolling_dice = np.array([True for _ in range(5)])

    def roll(self):
        self.dice = np.where(self.rolling_dice, np.random.randint(1, 7, size=5), self.dice)
        self.rolls += 1

        if self.rolls >= 3:
            print('end of turn')

    def get_user_dice_holds(self): 
        hold_arr = input()
        self.rolling_dice = hold_arr  

    def end_turn(self):
        self.get_user_scoring_choice()

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
        print(self.scorecard.total)                   
