# import pytest
# from ten_thousand.game_logic import GameLogic

# # Testing - Roll Dice
# # When rolling 1 to 6 dice ensure...
# # A sequence of correct length is returned
# # Each item in sequence is an integer with value between 1 and 6


# def test_roll_six():
#     roll = GameLogic.roll_dice(6)
#     assert len(roll) == 6
#     for value in roll:
#         assert 1 <= value <= 6


# def test_roll_five():
#     roll = GameLogic.roll_dice(5)
#     assert len(roll) == 5
#     for value in roll:
#         assert 1 <= value <= 6


# # Hey! test_roll_six and test_roll_five are REALLY similar
# # There's got to be a better way...


# @pytest.mark.parametrize(
#     "num_dice,expected_length",
#     [
#         (1, 1),
#         (2, 2),
#         (3, 3),
#         (4, 4),
#         (5, 5),
#         (6, 6),
#     ],
# )
# def test_all_valid_dice_rolls(num_dice, expected_length):
#     roll = GameLogic.roll_dice(num_dice)
#     assert len(roll) == expected_length
#     for value in roll:
#         assert 1 <= value <= 6

# @pytest.mark.parametrize(
#     "tuple,expected_score",
#     [
#         ([1, 1, 1, 1, 1, 1], 8000), # 6 pair
#         ([1, 2, 3, 4, 5, 6], 1500), # Straight
#         ([1, 1, 2, 2, 3, 3], 1000), # 3 pair
#         ([1, 1, 2, 3, 4, 5], 250), # Assorted 1s and 5s
#         ([1, 1, 1, 4, 4, 4], 2800), # Double Trips
#         ([1, 1, 1, 5, 5, 3], 1500), # Full House
#         ([2, 3, 4, 4, 6, 6], 0), # Farkle
#         ([1, 2, 4, 3, 3, 3], 400), # Leftover 1s
#         ([5, 2, 4, 3, 3, 3], 350), # Leftover 5s
#     ]
# )

# def test_scores(tuple, expected_score):
#     game = GameLogic()
#     score = game.calculate_score(tuple)
#     assert score == expected_score