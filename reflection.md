# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

Reflection
1. When completing the first game, clicking "New Game" does not reset the game. 
2. Input negative values or 0 returns Go Lower when it should be Go Higher as the expected range is between 1 and 100 (Normal Difficulty)
3. Difficulty logic does not make sense: number of attempts and number range in each level do not follow any specific trend (higher difficulty = larger range)
4. Input 99 says Go Higher but 100 says Go Lower


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| -1 or 0 | Go Higher | Go Lower | Guess is below secret, but hint is inverted|
| 99 then 100 | if 100 is not correct, then both 99 and 100 should return go lower| 99 returns Go Higher, 100 returns Go Lower, and the secret isn't 100 | TypeError caught internally. On even attempts the secret becomes a string, so guess is compared as text ("100" < "54") |
| 42 (secret is 54) | Go Higher  | Go Lower | Guess is higher secret, but hint is inverted |
| Click "New Game" after winning/losing | Game fully resets: new secret, score 0, attempts cleared, playable again | Secret and attempts reset but status, score, and history persist; game stays in won/lost state and won't play | None 

---

## 2. How did you use AI as a teammate?

- **Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?**

  - Claude

- **Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).**
  - The AI diagnosed why hints were unreliable: on even-numbered attempts the code converted the secret to a string (secret = str(st.session_state.secret)) before calling check_guess, forcing an int vs str comparison. In Python that fell back to lexicographic string comparison (e.g. "9" > "50" is True), so the hints were wrong on those turns. The AI suggested coercing both values to int inside check_guess and removing the str(secret) glitch so the secret is always passed as an integer. I verified this by confirming the existing pytest cases (test_guess_too_high, test_guess_too_low, test_winning_guess) still passed after the change.


- **Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).**
  - When fixing the wrong hints, the AI first suggested that coercing guess and secret to int in check_guess would "make the hints correct on every attempt." That was misleading — it fixed the int/string comparison glitch, but the hints were still wrong because of a separate swapped-message bug. I verified by testing again: guessing 1 still showed "Go LOWER" even after that change. Only after also swapping the hint text did the hints actually become correct. This showed one fix didn't fully solve the reported problem, despite the AI's claim.
---

## 3. Debugging and testing your fixes

- **How did you decide whether a bug was really fixed?**
  I confirmed a bug was fixed by reproducing the exact failing input and checking the new behavior, not just by reading the code. For the out-of-range bug I re-entered `-1` and `0` and confirmed they were now rejected with a clear message instead of returning a misleading hint. For the swapped-hint bug I guessed `1` and verified it now says "Go HIGHER!" instead of "Go LOWER!". I only considered a fix complete once the symptom was gone and the existing pytest suite still passed.

- **Describe at least one test you ran and what it showed you.**
  I ran python -m pytest tests/ and all 3 tests passed. This told me check_guess gives the right answer ("Win", "Too High", or "Too Low") and that moving my code into logic_utils.py didn't break anything. The pytests also show me that they only want check_guess to return a short result like "Win", not the full hint sentence. So I kept the hint wording in a separate function (get_hint_message), which let the tests pass while the game still showed messages to the player.

- **Did AI help you design or understand any tests? How?**
  Yes. The AI explained why the existing tests required `check_guess` to return only the outcome string and warned that returning a tuple would break them. It also suggested extra tests to try (like rejecting out-of-range numbers and decimals), which helped me understand what each function is supposed to do

---

## 4. What did you learn about Streamlit and state?

- **How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?**

  - Streamlit "reruns": everytime a user interact with the page, Streamlit app runs the entire Python file again
  - Session state: To preserve information across reruns, Streamlit provides session_state, which acts as per-user memory and stores values such as form inputs, counters, authentication status, or intermediate results. 
  - A useful analogy is that reruns redraw the page from scratch, while session state keeps a notebook of information that survives those redraws.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - One habit I want to continue is testing my code in small steps instead of generating an entire solution at once. By verifying each function and output incrementally, I was able to identify errors more quickly and better understand how the code worked.
 
- What is one thing you would do differently next time you work with AI on a coding task?
  - Next time, I would do a better job of tracking the changes and suggestions provided by AI throughout the project. When AI generates multiple code revisions, it can become overwhelming to remember what was changed and why, so maintaining clear notes or using version control more consistently would help me stay organized and debug issues more effectively.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - This project showed me that AI is a powerful tool for accelerating development and generating ideas, but it is not a substitute for understanding the code yourself. AI-generated solutions still require critical thinking, testing, and validation by the developer.
