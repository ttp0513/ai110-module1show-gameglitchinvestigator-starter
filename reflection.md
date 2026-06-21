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

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

  - Claude

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - The AI diagnosed why hints were unreliable: on even-numbered attempts the code converted the secret to a string (secret = str(st.session_state.secret)) before calling check_guess, forcing an int vs str comparison. In Python that fell back to lexicographic string comparison (e.g. "9" > "50" is True), so the hints were wrong on those turns. The AI suggested coercing both values to int inside check_guess and removing the str(secret) glitch so the secret is always passed as an integer. I verified this by confirming the existing pytest cases (test_guess_too_high, test_guess_too_low, test_winning_guess) still passed after the change.


- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - When fixing the wrong hints, the AI first suggested that coercing guess and secret to int in check_guess would "make the hints correct on every attempt." That was misleading — it fixed the int/string comparison glitch, but the hints were still wrong because of a separate swapped-message bug. I verified by testing again: guessing 1 still showed "Go LOWER" even after that change. Only after also swapping the hint text did the hints actually become correct. This showed one fix didn't fully solve the reported problem, despite the AI's claim.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
