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

- [x] **Describe the game's purpose.**
-  A Streamlit number-guessing game where the player tries to guess a secret number within a limited number of attempts, with "higher/lower" hints and a score.

- [x] **Detail which bugs you found.**
1. Out-of-range guesses such as `-1` or `0` were accepted as valid and returned a misleading "Go LOWER" hint, even though the secret number is only ever within the difficulty's range such as 1 to 50.
2. On even-numbered attempts the secret was converted to a string before being compared, forcing an `int`/`str` mismatch in `check_guess` that fell back to lexicographic string comparison (e.g. `"9" > "50"`) and produced wrong hints.
3. The hint text was swapped: a guess that was too high said "Go HIGHER!" and a guess that was too low said "Go LOWER!", so guessing `1` told the player to go lower.

- [x] **Explain what fixes you applied.**
1. Added an `is_in_range(value, low, high)` helper and updated `parse_guess` to call it, rejecting any guess outside the inclusive `[low, high]` range with the message "Enter a number between {low} and {high}." This stops invalid guesses from reaching `check_guess` and producing false hints.
2. Hardened `check_guess` to always coerce `guess` and `secret` to `int` so comparisons are numeric, and removed the even-attempt `str(secret)` glitch so the secret is always passed as an integer.
3. Swapped the hint text to match the outcome: too high now says "📉 Go LOWER!" and too low says "📈 Go HIGHER!".


## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [x] **Guess History.** Added a "📜 Guess History" panel that lists every guess made in the current game (most recent first), showing the attempt number, the guessed value, the outcome (Win / Too High / Too Low / Invalid), and the hint message. Each guess is stored as a structured entry, and starting a new game clears the history, score, and status for a clean slate.
- [x] **Whole-number validation.** `parse_guess` now rejects decimal input (e.g. `12.9`) with the message "Enter a whole number (no decimals)." instead of silently flooring it, so only valid integer guesses are accepted.
