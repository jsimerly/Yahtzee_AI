import numpy as np

class ScoreCard:
    def __init__(self) -> None:       
        """ Array Choices
        0: Ace
        1: Twos
        2: Threes
        3: Fours
        4: Fives
        5: Sixes
        6: 3 of a Kind
        7: 4 of a kind
        8: Full House
        9: Sm Straight
        10: Lg Straight
        11: Chance
        12: Yahtzee
        13: Bonus Yahztee """

        self.available = np.array([False for _ in range(14)])
        self.points = np.array([0 for _ in range(14)])
        self.total = 0

    def add_score(self, choice: int, points: int) -> bool:
        if self.available[choice]:
            self.available[choice] = False
            self.points[choice] = points

            self.total += points
            return True
        return False
    
    def ace(self, dice: np.ndarray) -> tuple[int, bool]:
        return dice[dice == 1].sum(), True
        
    def two(self, dice: np.ndarray) -> tuple[int, bool]:
        return dice[dice == 2].sum()
    
    def three(self, dice: np.ndarray) -> tuple[int, bool]:
        return dice[dice == 3].sum()
    
    def four(self, dice: np.ndarray) -> tuple[int, bool]:
        return dice[dice == 4].sum()
    
    def five(self, dice: np.ndarray) -> tuple[int, bool]:
        return dice[dice == 5].sum()
    
    def six(self, dice: np.ndarray) -> tuple[int, bool]:
        return dice[dice == 6].sum()
    
    def three_of_a_kind(self, dice: np.ndarray) -> tuple[int, bool]:
        counts = np.bincount(dice)
        max_count = np.max(counts)
        if max_count >= 3:
            number = np.argmax(counts)
            return number * max_count
        return None, False
    
    def three_of_a_kind(self, dice: np.ndarray) -> tuple[int, bool]:
        counts = np.bincount(dice)
        max_count = np.max(counts)
        if max_count >= 4:
            number = np.argmax(counts)
            return number * max_count
        return None, False
    
    def full_house(self, dice: np.ndarray) -> tuple[int, bool]:
        counts = np.bincount(dice)
        if 2 in counts and 3 in counts:
            return 25, True
        return None, False
    
    def sm_straight(self, dice: np.ndarray) -> tuple[int, bool]:
        # use a fixed sliding window here instead
        sorted_dice = np.sort(dice)
        for i in range(4):
            if (sorted_dice[i] != sorted_dice[i+1]+1):
                return None, False
        return 30, True
    
    def lg_straight(self, dice: np.ndarray) -> tuple[int, bool]:
        sorted_dice = np.sort(dice)
        # fixed sliding window
        return 40, False

    def chance(self, dice: np.ndarray) -> tuple[int, bool]:
        return dice.sum(), True
    
    def yahtzee(self, dice: np.ndarray) -> tuple[int, bool]:
        if len(np.unique(dice)) != 1:
            return None, False
        return 50, True
    



    
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
        score_now = input()
        if score_now:
            self.end_turn()
        
        for i in range(5):
            hold = bool(input())
            if hold:
                self.rolling_dice[i] = False
            else:
                self.rolling_dice[i] = True

    def end_turn(self):
        self.get_user_scoring_choice()

        self.round += 1
        if self.round > 13:
            self.end_game()

    def get_user_scoring_choice(self):
        choice = int(input())
        updated = self.scorecard.add_score(choice)
        if not updated:
            self.get_user_scoring_choice()
            

    def end_game(self):
        print(self.scorecard.total)

    def calculate_score(self, choice):
        ...

                   

if __name__ == '__main__':
    client = GameClient(1)
