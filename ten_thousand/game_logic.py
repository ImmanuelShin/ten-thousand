import random
from collections import Counter

class GameLogic:
  """
  A class representing the game logic for a dice game.
  
  This class provides methods for rolling dice and calculating scores
  based on specific game rules.
  """

  @staticmethod
  def calculate_score(dice):
    """
    Calculate and return the score for a given dice roll.

    The scoring is based on specific rules:
    - A straight set (1-6) returns 1500.
    - Three pairs return 1500.
    - N of a kind (where N > 3) for any number except 1 gives that number multiplied by 100, 
      then multiplied by (N - 2).
    - For the number 1, N of a kind gives 1000 multiplied by (N - 2).
    - A set of two pairs of 3 returns the sum of the N of a kind values for both sets.
    - Remaining 1s and 5s add 100 and 50 points each, respectively.

    Parameters:
    dice_roll (tuple of int): A tuple representing the dice roll.

    Returns:
    int: The calculated score.
    """

    score = 0
    rolls = Counter(dice)

    # Straight
    if set(dice) == set(range(1, 7)):
      return 1500
    
    # Three Pair
    if len(rolls) == 3 and all(roll == 2 for roll in rolls.values()):
      return 1500

    for num, roll in rolls.items():
      if roll >= 3:
          if num == 1:
              if roll == 3:
                  score += 1000  # Three 1s
              else:
                  score += 1000 * (roll - 2)  # More than three 1s
          else:
              if roll == 3:
                  score += num * 100
              else:
                  score += num * 100 * (roll - 2)

    if rolls[1] < 3:
        score += rolls[1] * 100
    if rolls[5] < 3:
        score += rolls[5] * 50

    return score
  
  @staticmethod
  def roll_dice(dice):
    """
    Roll a specified number of dice and return the results.

    Parameters:
    dice (int): The number of dice to roll.

    Returns:
    tuple: A tuple containing the results of each dice roll.
    """
    return tuple(random.randint(1, 6) for _ in range(0,dice))