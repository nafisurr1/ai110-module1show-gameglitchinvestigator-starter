from pathlib import Path

import pytest

from logic_utils import check_guess

APP_PATH = str(Path(__file__).resolve().parent.parent / "app.py")

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_too_high_hint_says_go_lower():
    # Bug 1: a guess of 60 against a secret of 50 is too high, so the player
    # must be told to go LOWER (the original code said "Go HIGHER!").
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message
    assert "HIGHER" not in message

def test_too_low_hint_says_go_higher():
    # Bug 1: a guess of 40 against a secret of 50 is too low, so the player
    # must be told to go HIGHER (the original code said "Go LOWER!").
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message
    assert "LOWER" not in message

def test_check_guess_compares_numbers_not_text():
    # Bug 2: compared as text, "9" > "50" and "100" < "50". As numbers, 9 is
    # below 50 and 100 is above it.
    assert check_guess(9, 50)[0] == "Too Low"
    assert check_guess(100, 50)[0] == "Too High"

def test_app_hints_stay_numeric_on_every_attempt():
    # Bug 2: app.py turned the secret into a str on even attempts, so the guess was
    # compared as text. The first Submit counts as attempt 2, so even and odd
    # attempts both run here. With a secret of 50: 9 must say HIGHER, 100 must say LOWER.
    testing = pytest.importorskip("streamlit.testing.v1")
    at = testing.AppTest.from_file(APP_PATH, default_timeout=10).run()
    at.session_state["secret"] = 50

    for raw, expected in [("9", "HIGHER"), ("100", "LOWER"), ("100", "LOWER"), ("9", "HIGHER")]:
        at.text_input(key="guess_input_Normal").set_value(raw)
        at.button[0].click().run()
        assert expected in at.warning[0].value, (
            f"attempt {at.session_state['attempts']}: guess {raw} vs secret 50 "
            f"showed {at.warning[0].value!r}"
        )
