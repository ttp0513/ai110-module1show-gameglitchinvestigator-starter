from logic_utils import (
    get_range_for_difficulty,
    is_in_range,
    parse_guess,
    check_guess,
    get_hint_message,
    update_score,
)


# --- check_guess ---------------------------------------------------------

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_check_guess_coerces_strings():
    # Values are coerced to int, so a string secret still compares numerically
    # (the old bug compared "9" > "50" as text and got it wrong)
    assert check_guess("9", "50") == "Too Low"
    assert check_guess(50, "50") == "Win"
    assert check_guess("100", "54") == "Too High"


# --- get_hint_message ----------------------------------------------------

def test_hint_message_matches_outcome():
    # Too high -> go lower, too low -> go higher (the swapped-hint bug fix)
    assert "LOWER" in get_hint_message("Too High")
    assert "HIGHER" in get_hint_message("Too Low")
    assert "Correct" in get_hint_message("Win")

def test_hint_message_unknown_outcome():
    assert get_hint_message("Invalid") == ""


# --- get_range_for_difficulty -------------------------------------------

def test_difficulty_ranges():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 50)
    assert get_range_for_difficulty("Hard") == (1, 100)

def test_difficulty_default_range():
    assert get_range_for_difficulty("Unknown") == (1, 100)


# --- is_in_range ---------------------------------------------------------

def test_is_in_range_bounds_inclusive():
    assert is_in_range(1, 1, 50) is True
    assert is_in_range(50, 1, 50) is True

def test_is_in_range_out_of_bounds():
    assert is_in_range(0, 1, 50) is False
    assert is_in_range(-1, 1, 50) is False
    assert is_in_range(51, 1, 50) is False


# --- parse_guess ---------------------------------------------------------

def test_parse_guess_valid():
    ok, value, err = parse_guess("25", 1, 50)
    assert ok is True
    assert value == 25
    assert err is None

def test_parse_guess_rejects_zero_and_negative():
    # The original bug: -1 and 0 were accepted as valid guesses
    ok, value, err = parse_guess("0", 1, 50)
    assert ok is False
    assert value is None
    assert "between 1 and 50" in err

    assert parse_guess("-1", 1, 50)[0] is False

def test_parse_guess_rejects_above_range():
    ok, value, err = parse_guess("51", 1, 50)
    assert ok is False

def test_parse_guess_empty_and_none():
    assert parse_guess("", 1, 50)[0] is False
    assert parse_guess(None, 1, 50)[0] is False

def test_parse_guess_not_a_number():
    ok, value, err = parse_guess("abc", 1, 50)
    assert ok is False
    assert err == "That is not a number."

def test_parse_guess_rejects_decimals():
    # Whole numbers only: "12.9" is rejected, not floored to 12
    ok, value, err = parse_guess("12.9", 1, 50)
    assert ok is False
    assert value is None
    assert "whole number" in err


# --- update_score --------------------------------------------------------

def test_update_score_win_awards_points():
    # Winning on attempt 1 should add points
    assert update_score(0, "Win", 1) > 0

def test_update_score_win_minimum_floor():
    # Late wins never drop below the +10 floor
    assert update_score(0, "Win", 20) == 10

def test_update_score_too_low_penalty():
    assert update_score(100, "Too Low", 3) == 95

def test_update_score_unknown_outcome_unchanged():
    # An outcome like "Invalid" should not change the score
    assert update_score(42, "Invalid", 1) == 42
