# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Secret is 50; I guess 60, then 40 | Guess 60 is too high, so the hint should say to go LOWER. Guess 40 is too low, so it should say to go HIGHER. | The hints are backwards: 60 shows "📈 Go HIGHER!" and 40 shows "📉 Go LOWER!". | No error. `check_guess(100, 50)` returns `('Too High', '📈 Go HIGHER!')`. |
| Any guess on an even-numbered attempt (the first Submit is already attempt 2 because `attempts` starts at 1 and is incremented before the check) | The comparison should be numeric on every attempt: 9 against a secret of 50 is "Too Low". | `app.py` casts the secret to a `str` on even attempts, so `check_guess` falls into its `TypeError` branch and compares text: 9 against `"50"` is "Too High" and 100 against `"50"` is "Too Low". | No error; the `except TypeError` fallback hides it. `check_guess(9, '50')` returns `('Too High', '📈 Go HIGHER!')`. |
| Win a game, click "New Game 🔁", then submit a guess | A fresh game starts: status, score and history reset, and the new guess is checked. | The new guess is rejected with "You already won. Start a new game to play again." because `status` is still `won`. Score (70) and history also carry over, `attempts` resets to 0 instead of 1, and the new secret ignores the difficulty range. | No error. After New Game: `status = won`, `attempts = 0`, `score = 70`, `history = [50]`. |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

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
