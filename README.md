# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

**Purpose.** A Streamlit number-guessing game. The app picks a secret number for the chosen difficulty (Easy 1 to 20, Normal 1 to 100, Hard 1 to 50), the player has a limited number of attempts, and after each guess the game says whether to go higher or lower until the player wins or runs out of attempts. The starter code was AI-generated and full of glitches, so the project is about finding, fixing and testing them.

**Bugs found.**

1. **Reversed hints.** A guess above the secret said "Go HIGHER!" and a guess below it said "Go LOWER!".
2. **Secret compared as text on even attempts.** `app.py` turned the secret into a `str` on even-numbered attempts, so `check_guess` fell into an `except TypeError` fallback and compared the numbers as text (9 against `"50"` came out as "Too High").
3. **New Game does not fully reset.** After a win, New Game leaves the status as `won`, so the next guess is rejected with "You already won". Score and history also carry over.

**Fixes applied.**

- Moved `get_range_for_difficulty`, `parse_guess`, `check_guess` and `update_score` out of `app.py` into `logic_utils.py`, and imported them in `app.py`.
- Swapped the hint messages so a guess that is too high says "Go LOWER!" and a guess that is too low says "Go HIGHER!".
- Always pass the secret to `check_guess` as an int and deleted the text-comparison fallback.
- Added tests for both fixes, including one that drives the real app with Streamlit's `AppTest` on even and odd attempts.

**Not fixed yet.** Bug 3 (New Game reset) is still open and marked with a `FIXME` in `app.py`. I also noticed that the "Attempts left" count starts one lower than the attempts allowed, and that the guess prompt always says "between 1 and 100" whatever the difficulty.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Run `python -m streamlit run app.py` and open the local URL. The sidebar shows the difficulty (Normal: range 1 to 100, 8 attempts allowed).
2. Open the "Developer Debug Info" panel to see the secret number. In my run the secret was 39.
3. Type 9 and click "Submit Guess 🚀". The game shows "📈 Go HIGHER!", which is correct because 9 is below 39.
4. Type 95, then 100, and submit each one. Both show "📉 Go LOWER!", on odd and even attempts alike, because the guess is now always compared as a number.
5. Type 39 and submit. The game shows "🎉 Correct!", throws balloons, and reports "You won! The secret was 39. Final score: 35".

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ pytest -v
collected 7 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 14%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 28%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 42%]
tests/test_game_logic.py::test_too_high_hint_says_go_lower PASSED        [ 57%]
tests/test_game_logic.py::test_too_low_hint_says_go_higher PASSED        [ 71%]
tests/test_game_logic.py::test_check_guess_compares_numbers_not_text PASSED [ 85%]
tests/test_game_logic.py::test_app_hints_stay_numeric_on_every_attempt PASSED [100%]

============================== 7 passed in 1.45s ===============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
