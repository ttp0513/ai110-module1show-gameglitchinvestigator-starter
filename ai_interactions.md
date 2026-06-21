# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the agent (Claude) to fix the game's bugs, refactor the logic out of the UI, add new features, and generate test cases. Specific multi-step tasks included: move all game logic from `app.py` into `logic_utils.py`, add a Guess History feature, add whole-number input validation, and generate pytest cases that cover all the features.

**What did the agent do?**

- Moved `get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score` (plus new `is_in_range` and `get_hint_message`) into `logic_utils.py`, and updated `app.py` to import them so the app.py file no longer defines logic.
- Fixed the bugs: out-of-range/decimal input validation, the `int`/`str` comparison glitch in `check_guess`, and the swapped hint text.
- Added the Guess History panel and made "New Game" reset history, score, and status.
- Generated an expanded `tests/test_game_logic.py` covering `check_guess`, `get_hint_message`, `get_range_for_difficulty`, `is_in_range`, `parse_guess`, and `update_score`, then ran `python -m pytest tests/`.

**What did you have to verify or fix manually?**

- The agent initially claimed coercing values to `int` in `check_guess` would make all hints correct, but I verified by guessing `1` that the hints were still wrong; the real fix also required swapping the hint text.
- I confirmed each fix by reproducing the original failing inputs (`-1`, `0`, `12.9`, guessing `1`) in the running app rather than trusting the agent's word.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Out-of-range / zero / negative guess | "Generate a pytest case that rejects values outside of expected range" | `test_parse_guess_rejects_zero_and_negative` asserts `parse_guess("0", 1, 50)` and `parse_guess("-1", 1, 50)` return `ok=False` with a "between 1 and 50" message | Yes | This was the original bug, so the test confirms invalid guesses are rejected before reaching `check_guess`. |
| Decimal input | "Generate a pytest case that captures only integer"| `test_parse_guess_rejects_decimals`  asserts `parse_guess("12.9", 1, 50)` returns `ok=False` with a "whole number" message | Yes | Verifies decimals are rejected instead of being silently floored to an int, matching the whole-number stretch feature. |
| String vs int comparison | "Generate a pytest case that check strings are coerced to integer before comparison" | `test_check_guess_coerces_strings` asserts `check_guess("9", "50") == "Too Low"` and `check_guess("100", "54") == "Too High"` | Yes | Confirms the int-coercion fix; without it, text comparison would wrongly rank "100" below "54". |
| Correct hint direction | "Generate a pytest case that check hints are provided correctly" | `test_hint_message_matches_outcome` asserts "Too High" maps to "LOWER" and "Too Low" maps to "HIGHER" | Yes | Locks in the swapped-hint fix so a too-high guess always tells the player to go lower. |
| Score floor on late win | "Generate a pytest case that check score is not lower than 10 points for a late win"| `test_update_score_win_minimum_floor` asserts `update_score(0, "Win", 20) == 10` | Yes | Checks that a late win never awards fewer than the +10 minimum points. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
