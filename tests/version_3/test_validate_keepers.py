import pytest
from ten_thousand.game_logic import GameLogic

pytestmark = [pytest.mark.version_3]


def test_validate_legal_keepers():
    game_logic = GameLogic()
    roll = (1, 2, 3, 4, 5)
    keepers = (5, 1)
    actual, bool = game_logic.validate_keepers(roll, keepers)
    expected = True
    assert actual == expected


def test_validate_illegal_keepers():
    game_logic = GameLogic()
    roll = (1, 2, 3, 4, 5)
    keepers = (1, 1, 1, 1, 1)
    actual, bool = game_logic.validate_keepers(roll, keepers)
    expected = False
    assert actual == expected


def test_validate_illegal_overflow():
    game_logic = GameLogic()
    roll = (1,)
    keepers = (1, 1, 1, 1, 1, 1)
    actual, bool = game_logic.validate_keepers(roll, keepers)
    expected = False
    assert actual == expected
