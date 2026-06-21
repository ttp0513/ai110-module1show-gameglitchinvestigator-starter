import random
import streamlit as st

# CHANGED: game logic moved into logic_utils.py; app.py is now UI-only.
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    get_hint_message,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)
# CHANGED: Adjust attempts based on difficulty
attempt_limit_map = {
    "Easy": 8,
    "Normal": 7,
    "Hard": 6,
}

attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between 1 and 100. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(1, 100)
    # CHANGED: reset history, score and status so a new game starts clean.
    st.session_state.history = []
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    # CHANGED: pass the difficulty's range so out-of-range guesses are rejected.
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        # CHANGED: record invalid guesses as structured history entries too.
        st.session_state.history.append(
            {
                "attempt": st.session_state.attempts,
                "guess": raw_guess,
                "outcome": "Invalid",
                "message": err,
            }
        )
        st.error(err)
    else:
        # CHANGED: removed the even-attempt str(secret) glitch that forced an
        # int/str mismatch in check_guess. The secret is now always passed as-is.
        secret = st.session_state.secret

        # CHANGED: check_guess now returns only the outcome; the hint text comes
        # from get_hint_message so the logic stays UI-free in logic_utils.py.
        outcome = check_guess(guess_int, secret)
        message = get_hint_message(outcome)

        # CHANGED: store each guess with its outcome and hint so the history
        # feature can display what happened on every attempt.
        st.session_state.history.append(
            {
                "attempt": st.session_state.attempts,
                "guess": guess_int,
                "outcome": outcome,
                "message": message,
            }
        )

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()

# CHANGED: added a Guess History feature that lists every past guess this game,
# most recent first, with its outcome and hint.
st.subheader("📜 Guess History")
if not st.session_state.history:
    st.caption("No guesses yet. Make your first guess above!")
else:
    for entry in reversed(st.session_state.history):
        st.write(
            f"#{entry['attempt']} — `{entry['guess']}` → "
            f"**{entry['outcome']}** {entry['message']}"
        )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
