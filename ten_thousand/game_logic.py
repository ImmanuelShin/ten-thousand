import random, re
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
    Calculate and return the score for a given dice roll and determine if it's a hot dice scenario.

    The scoring is based on specific rules:
    - A straight set (1-6) returns 1500.
    - Three pairs return 1500.
    - N of a kind (where N > 3) for any number except 1 gives that number multiplied by 100, 
      then multiplied by (N - 2).
    - For the number 1, N of a kind gives 1000 multiplied by (N - 2).
    - A set of two pairs of 3 returns the sum of the N of a kind values for both sets.
    - Remaining 1s and 5s add 100 and 50 points each, respectively.

    Parameters:
    dice (tuple of int): A tuple representing the dice roll.

    Returns:
    tuple of (int, bool): The calculated score and a boolean indicating if it's a hot dice scenario.
    """

    score = 0
    rolls = Counter(dice)
    hot_count = 0

    # Straight
    if set(dice) == set(range(1, 7)):
      return 1500, True
    
    # Three Pair
    if len(rolls) == 3 and all(roll == 2 for roll in rolls.values()):
      return 1500, True

    for num, roll in rolls.items():
      if roll >= 3:
        hot_count += roll
        if num == 1:
          score += 1000 * (roll - 2) # N of a kind 1
        else:
          score += num * 100 * (roll - 2) # N of a kind others

    # Leftover 1s and 5s
    if rolls[1] < 3:
        score += rolls[1] * 100
        hot_count += rolls[1]
    if rolls[5] < 3:
        hot_count += rolls[5]
        score += rolls[5] * 50

    return score, hot_count == len(dice)
  
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
  
  def set_aside_dice(self, dice_roll):
    """
    Allows the player to select dice to set aside for scoring.

    Parameters:
    dice_roll (tuple of int): The dice roll from which the player selects.

    Returns:
    tuple of int: The dice selected by the player for scoring.
    """

    while True:
      try:
        kept_dice_input = input("Enter the dice you want to keep (e.g., 156 for keeping 1, 5, and 6): ")
        if kept_dice_input.lower() == 'q':
          raise KeyboardInterrupt("Player chose to quit the game.")
        kept_dice_numbers = re.findall(r'\d', kept_dice_input)
        kept_dice = tuple(int(d) for d in kept_dice_numbers)

        if not all(dice_roll.count(d) >= kept_dice.count(d) for d in kept_dice):
          print("Invalid selection. Please choose dice from the roll.")
          continue
        roll_score, _ = self.calculate_score(kept_dice)
        if roll_score > 0:
          return kept_dice
        else:
          print("At least one scoring die must be chosen.")
      except ValueError:
        print("Invalid input. Please choose numbers corresponding to dice.")
  
class Game:
  """
  A class representing the main game logic and flow.

  Methods:
  - play_round: Conducts a single round of the game for a given player.
  - set_aside_dice: Allows the player to select dice to set aside for scoring.
  - bank_score: Adds the round score to the player's total score and checks for game end conditions.
  - setup_players: Initializes player information for the game.
  - start_game: Starts the game, providing options to start, learn the rules, or quit.
  - play_game: Conducts the game rounds, iterating through players.
  - show_tutorial: Displays the game rules and instructions.
  - display_final_scores: Displays the final scores of the players at the end of the game.
  """
  
  def __init__(self):
    """
    Initialize the Game class.

    Attributes:
    players (list): A list of players in the game.
    round_number (int): The current round number.
    game_logic (GameLogic): An instance of the GameLogic class.
    end_phase (bool): Indicates if the game is in the end phase.
    """
    self.players = []
    self.round_number = 1
    self.game_logic = GameLogic()
    self.end_phase = False

  def play_round(self, player):
    """
    Conducts a single round of the game for a given player.

    Parameters:
    player (dict): A dictionary containing player information.

    Returns:
    bool: True if the game ends, False otherwise.
    """

    print(f"\n--- Round {self.round_number} ---")
    dice_left = 6
    round_score = 0
    
    while dice_left > 0:
      dice_roll = self.handle_dice_roll(player, dice_left)
      roll_score, is_hot = self.game_logic.calculate_score(dice_roll)
      
      if roll_score == 0:
        print(f"Farkle! No scoring dice. {player['name']}'s turn is over.\n")
        round_score = 0
        break  # Ends the current round
      elif is_hot:
        print(f"Hot Dice! {player['name']} receives another turn!")
        round_score += roll_score
        if self.bank_score(player, round_score):
          return True  # End game
        dice_left = 6
        continue
      round_score, dice_left = self.process_player_decision(player, dice_roll, round_score, dice_left)
      if round_score is None:  # Indicates game end or interruption
        return True
    return False # Continue game
  
  def handle_dice_roll(self, player, dice_left):
    """
    Handles the dice rolling action for a player.

    Parameters:
    player (dict): A dictionary containing player information.
    dice_left (int): The number of dice the player is rolling.

    Returns:
    tuple of int: The result of the dice roll.
    """
    dice_roll = self.game_logic.roll_dice(dice_left)
    print(f"{player['name']}'s roll:", dice_roll)
    return dice_roll
  
  def process_player_decision(self, player, dice_roll, round_score, dice_left):
    """
    Processes the player's decision after a dice roll, including setting aside dice for scoring
    and deciding whether to roll again or bank the score.

    Parameters:
    player (dict): A dictionary containing player information.
    dice_roll (tuple of int): The result of the player's dice roll.
    round_score (int): The player's score for the current round.
    dice_left (int): The number of dice remaining for the player to roll.

    Returns:
    tuple (int, int or None): A tuple containing the updated round score and remaining dice.
                               If the game or round ends, returns (None, None) or (0, 0).
    """
    try:
      chosen_dice = self.game_logic.set_aside_dice(dice_roll)
    except KeyboardInterrupt:
      print("\nGame ended by player.")
      return None, None  # Ends the game

    print(f"{player['name']} has chosen to keep:", chosen_dice)
    roll_score, _ = self.game_logic.calculate_score(chosen_dice)
    round_score += roll_score
    dice_left -= len(chosen_dice)

    player_decision = input(f"Your round score is {round_score}. (R)oll again or (b)ank score? (r/b): ")
    if player_decision.lower() == 'b':
      if self.bank_score(player, round_score):
        return None, None  # End game
      return 0, 0
    elif player_decision.lower() == 'q':
      print("Thank you for playing! Ending the game.")
      return None, None  # End game

    return round_score, dice_left

  def bank_score(self, player, score):
    """
    Adds the round score to the player's total score and checks for game end conditions.

    Parameters:
    player (dict): The player's information.
    score (int): The score to be added to the player's total.

    Returns:
    bool: True if the game ends, False otherwise.
    """

    player['score'] += score
    print(f"{player['name']} banks their score. Total score: {player['score']}")

    if player['score'] == 10000:
      print(f"\n{player['name']} wins the game with exactly 10,000 points!")
      return True  # End game
    elif player['score'] > 10000:
      self.end_phase = True  # Enter last round
    return False
  
  def setup_players(self, num_players):
    """
    Initializes player information for the game.

    Parameters:
    num_players (int): The number of players in the game.
    """

    self.players = []
    for i in range(num_players):
      name = input(f"Enter name for Player {i + 1}: ")
      self.players.append({'name': name, 'score': 0})
  
  def start_game(self):
    """
    Starts the game, providing options to start, learn the rules, or quit.
    """

    while True:
      print(
'''
Welcome to the Dice Game!
Choose an option:
(S)tart the game
(T)utorial
(Q)uit
'''
      )

      choice = input("Enter your choice: ").lower()

      if choice == 's':
        while True:
          try:
            num_players = int(input("Enter the number of players: "))
            if num_players > 0:
              break
            else:
              print("Please enter a positive number.")
          except ValueError:
            print("Invalid input. Please enter a valid number.")
        self.setup_players(num_players)
        self.play_game()
        self.display_final_scores()
        break
      elif choice == 't':
        self.show_tutorial()
      elif choice == 'q':
        print("Thank you for playing!")
        break
      else:
        print("Invalid choice, please try again.")

  def play_game(self):
    """
    Conducts the game rounds, iterating through players.
    """

    self.round_number = 1
    while True:
      print(f"\nRound {self.round_number}")
      for player in self.players:
        print(f"\n{player['name']}'s turn. Score: {player['score']}")
        if self.play_round(player):
          return


      continue_game = input("Do you want to play another round? (y/n): ")
      if continue_game.lower() != 'y':
        break

      self.round_number += 1
      
  def show_tutorial(self):
    """
    Displays the game rules and instructions.
    """

    print(
'''
Game Rules:
1. A straight set (1-6) returns 1500 points.
2. Three pairs return 1500 points.
3. Three of a kind (except 1s) scores 100 times the dice number.
4. Three 1s score 1000 points.
5. Each additional dice in a set of three multiplies the score by 2.
   For example, four of a kind is double the three of a kind score.
6. Single 1s score 100 points each.
7. Single 5s score 50 points each.
8. A set of two triples scores the sum of the two triples' scores.

Scoring Examples:
Roll [1,1,1,5,5,2] can score 1000 (for three 1s) + 50 (for one 5) = 1050 points.
Roll [2,2,2,3,3,3] can score 200 (for three 2s) + 300 (for three 3s) = 500 points.

How to Play:
To play, roll the dice and choose which ones to keep for scoring.
You can choose to 'bank' your score or roll the remaining dice again.
If none of the dice rolled contribute to the score, it's a 'Farkle', and your turn ends.
The game continues until a player reaches a predetermined score (e.g., 10,000 points).
If you bank your score, your turn ends, and the next player rolls.
Remember, strategic dice selection and knowing when to bank your score is key!
'''
    )

  def display_final_scores(self):
    """
    Displays the final scores of the players at the end of the game.
    """

    print("\nThank you for playing the game!\n")
    print("Final Scores:")

    # Check for a winner with exactly 10,000 points
    exact_winner = next((player for player in self.players if player['score'] == 10000), None)

    if exact_winner:
      print(f"{exact_winner['name']}: {exact_winner['score']} pts (winner)")
      sorted_players = sorted((player for player in self.players if player != exact_winner), key=lambda x: x['score'], reverse=True)
    else:
      # If no exact 10,000 points winner, the highest scorer is the default winner
      highest_score = max(self.players, key=lambda x: x['score'])
      print(f"{highest_score['name']}: {highest_score['score']} pts (winner)")
      sorted_players = sorted((player for player in self.players if player != highest_score), key=lambda x: x['score'], reverse=True)

    for player in sorted_players:
        print(f"{player['name']}: {player['score']} pts")
    
if __name__ == "__main__":
  game = Game()
  game.start_game()