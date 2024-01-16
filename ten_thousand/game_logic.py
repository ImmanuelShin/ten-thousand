import random

class GameLogic:
  """
  A class to represent the game logic for a dice game, such as Dice 10000.

  This class provides methods for rolling dice and calculating scores based 
  on the outcome of the dice rolls.
  """

  @staticmethod
  def calculate_score(dice):
    """
    Calculate the score for a given roll of dice in Dice 10000.

    The score is calculated based on a set of rules which include straights,
    three pairs, sets of a kind (like three or more 1s), and leftover 1s and 5s.

    Parameters:
    dice (tuple): A tuple of integers representing the outcome of the dice roll.

    Returns:
    int: The calculated score for the given roll of dice.
    """

    score = 0
    rolls = [dice.count(i) for i in range(1,7)]

    # Straight
    if sorted(dice) == [1, 2, 3, 4, 5, 6]:
      return 1500
    
    # Three Pair
    if len([roll for roll in rolls if roll == 2]) == 3:
      return 1500

    # # Full House
    # if 3 in rolls and 2 in rolls and rolls.index(3) != rolls.index(2):
    #   return 1500
    
    # Double Trips
    if rolls.count(3) == 2:
        return sum([(1000 if i == 0 else (i + 1) * 100) for i, count in enumerate(rolls) if count == 3])
    
    for i in range(6):
      roll = rolls[i]
      # Sets of a kind
      if roll >= 3:
        base_score = 1000 if i == 0 else (i + 1) * 100
        score += base_score * (roll - 2)
        if i == 0 or i == 4:
          roll = 0 
      # Leftover 1s and 5s
      elif i == 0 or i == 4:
        score += (100 if i == 0 else 50) * roll

    return score
  
  @staticmethod
  def roll_dice(dice):
    """
    Calculate the score for a given roll of dice in Dice 10000.

    The score is calculated based on a set of rules which include straights,
    three pairs, sets of a kind (like three or more 1s), and leftover 1s and 5s.

    Parameters:
    dice (tuple): A tuple of integers representing the outcome of the dice roll.

    Returns:
    int: The calculated score for the given roll of dice.
    """
    return tuple(random.randint(1, 6) for _ in range(0,dice))