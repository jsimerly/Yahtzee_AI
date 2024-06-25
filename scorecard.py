import numpy as np
from typing import Callable
from enum import Enum

class ScoreOptions(Enum):
    ACE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    THREE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 7
    FULL_HOUSE = 8
    SM_STRAIGHT = 9
    LG_STRAIGHT = 10
    CHANCE = 11
    YAHTZEE = 12

class ScoreCard:
    def __init__(self) -> None:   
        self.available = np.array([False for _ in range(14)])
        self.points = np.array([0 for _ in range(14)])
        self.total = 0    

        self.option_methods: list[Callable] = [
            self.ace,               #0
            self.two,               #1
            self.three,             #2
            self.four,              #3
            self.five,              #4
            self.six,               #5
            self.three_of_a_kind,   #6
            self.four_of_a_kind,    #7
            self.full_house,        #8 
            self.sm_straight,       #9  
            self.lg_straight,       #10
            self.chance,            #11
            self.yahtzee,           #12    
        ]

    def add_score(self, choice: int, dice: np.ndarray) -> bool:
        choice_method = self.option_methods[choice]

        points, updated = choice_method(dice=dice)
        if not updated:
            return False

        if self.available[choice] or choice == ScoreOptions.YAHTZEE.value:
            self.available[choice] = False
            self.points[choice] = points

            self.total += points
            return points, True
        return None, False
        
    def ace(self, dice: np.ndarray) -> tuple[int, bool]:
        return dice[dice == 1].sum(), True
        
    def two(self, dice: np.ndarray) -> tuple[int, bool]:
        return dice[dice == 2].sum(), True
    
    def three(self, dice: np.ndarray) -> tuple[int, bool]:
        return dice[dice == 3].sum(), True
    
    def four(self, dice: np.ndarray) -> tuple[int, bool]:
        return dice[dice == 4].sum(), True
    
    def five(self, dice: np.ndarray) -> tuple[int, bool]:
        return dice[dice == 5].sum(), True
    
    def six(self, dice: np.ndarray) -> tuple[int, bool]:
        return dice[dice == 6].sum(), True
    
    def three_of_a_kind(self, dice: np.ndarray) -> tuple[int, bool]:
        counts = np.bincount(dice)
        max_count = np.max(counts)
        if max_count >= 3:
            number = np.argmax(counts)
            return number * max_count, True
        return None, False
    
    def four_of_a_kind(self, dice: np.ndarray) -> tuple[int, bool]:
        counts = np.bincount(dice)
        max_count = np.max(counts)
        if max_count >= 4:
            number = np.argmax(counts)
            return number * max_count, True
        return None, False
    
    def full_house(self, dice: np.ndarray) -> tuple[int, bool]:
        counts = np.bincount(dice)
        if 2 in counts and 3 in counts:
            return 25, True
        return None, False
    
    def sm_straight(self, dice: np.ndarray) -> tuple[int, bool]:
        sorted_dice = np.sort(dice)
        for i in range(4):
            if (sorted_dice[i] != sorted_dice[i+1]+1):
                return None, False
        return 30, True
    
    def lg_straight(self, dice: np.ndarray) -> tuple[int, bool]:
        sorted_dice = np.sort(dice)
        for i in range(5):
            if (sorted_dice[i] != sorted_dice[i+1]+1):
                return None, False
        return 40, False

    def chance(self, dice: np.ndarray) -> tuple[int, bool]:
        return dice.sum(), True
    
    def yahtzee(self, dice: np.ndarray) -> tuple[int, bool]:
        if len(np.unique(dice)) != 1:
            return None, False
        
        if not self.available[ScoreOptions.YAHTZEE.value]:
            return 100, True
        return 50, True