import random

class GameLogic:

  @staticmethod
  def calculate_score(dice):
    score = 0
    rolls = [dice.count(i) for i in range(1,7)]
    if sorted(dice) == [1, 2, 3, 4, 5, 6]:
      return 1500
    
    if len([roll for roll in rolls if roll == 2]) == 3:
      return 1500

    if any(rolls.count(x) == 3 for x in range(1, 7)) and any(rolls.count(x) == 2 for x in range(1, 7)):
      return 1500
    
    if rolls.count(3) == 2:
        double_trips_score = sum([(1000 if i == 0 else (i + 1) * 100) for i, count in enumerate(rolls) if count == 3])
        return double_trips_score * 2
    
    for i in range(6):
      roll = rolls[i]
      if roll >= 3:
        base_score = 1000 if i == 0 else (i + 1) * 100
        score += base_score * (2 ** (roll - 3))
        if i == 0 or i == 4:
          count = 0 
      elif i == 0 or i == 4:
        score += (100 if i == 0 else 50) * count

    return score
  
  @staticmethod
  def roll_dice(dice):
    return tuple(random.randint(1, 6) for _ in range(0,dice))
  
# game = GameLogic()
# tuple = game.roll_dice(6)  # Example: Rolls 6 dice
# print(tuple)
# print(game.calculate_score([1, 1, 2, 2, 3, 3]))