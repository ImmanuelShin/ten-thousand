import random

class GameLogic:

  @staticmethod
  def calculate_score(dice):
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
    return tuple(random.randint(1, 6) for _ in range(0,dice))