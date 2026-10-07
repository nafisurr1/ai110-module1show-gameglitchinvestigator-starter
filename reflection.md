# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**What the game looked like.** The app loaded without errors and looked playable: a sidebar with Difficulty, a "Make a guess" box, Submit Guess and New Game buttons, and a Developer Debug Info panel that shows the secret. The problems only showed up once I ran guesses through it, because the hints did not agree with the secret in the debug panel. The "Attempts left" count also started one lower than the 8 attempts allowed.

**Bugs I noticed at the start.** First, the hints were backwards: a guess of 60 against a secret of 50 said "Go HIGHER!". Second, on even-numbered attempts the secret was turned into a string, so guesses like 9 and 100 were compared as text and gave the wrong outcome. Third, clicking New Game after a win did not reset the game, so the next guess was rejected with "You already won".

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

**AI tools used.** One AI coding assistant, working in agent mode: it read `app.py`, `logic_utils.py` and the tests, edited the files, ran `pytest`, and drove the Streamlit app. I did not use any other AI tool on this project.

**A suggestion that was correct (bug 1, the reversed hints).** The assistant pointed out that the outcome labels in `check_guess` were right ("Too High" for 60 vs 50) and only the messages were swapped, which is why the three starter tests, which only look at the outcome, could never catch a lying hint. Its suggestion was to assert on the message text as well, so it wrote `test_too_high_hint_says_go_lower` and `test_too_low_hint_says_go_higher` first and then swapped the messages. That was correct because the starter tests stayed green while the hints were wrong, so only message-level tests could fail for the right reason. I verified it by running pytest before the fix (2 failed, 3 passed) and after (5 passed), and then in the live game, where a guess above the secret now says "Go LOWER!".

**A suggestion not accepted as written (bug 2, the str secret).** The AI-written starter code handled the str secret with an `except TypeError` fallback in `check_guess` that compares the guess as text. The tempting fix was to keep that fallback and only swap its messages, but I rejected it because the fallback only exists to cope with `app.py` turning the secret into a `str` on even attempts, and it hid the real bug: 9 against `"50"` came out as "Too High". I removed the cast in `app.py` and deleted the fallback so `check_guess` always compares two ints. I verified it with an `AppTest` test that failed before the fix ("attempt 2: guess 9 vs secret 50 showed '📉 Go LOWER!'") and passes after, and in the live game on an even attempt.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

**How I decided a bug was fixed.** I wrote the test for each bug first and watched it fail on the buggy code, then made the change and watched it pass, so a green run actually meant something. After that I played the real app and compared the hints against the secret shown in the Developer Debug Info panel.

**Tests I ran.** I ran `pytest` at each step. The starter tests failed first with `NotImplementedError` because the logic was still stubbed, and they passed (3 passed) once I moved the functions into `logic_utils.py`. The bug 1 tests then failed (2 failed, 3 passed) and passed after the fix (5 passed), and the final run is 7 passed. In the live game (secret 39) a guess of 9 said "Go HIGHER!", 95 said "Go LOWER!", 100 on an even attempt said "Go LOWER!", and 39 won with a final score of 35.

**How AI helped with the tests.** The assistant wrote the tests, and it also showed me a limit of the obvious test. A plain `check_guess(9, 50)` unit test passes even with bug 2 present, because the `str()` cast lives in `app.py`, so it added `test_app_hints_stay_numeric_on_every_attempt`, which drives the real app with Streamlit's `AppTest` on both even and odd attempts. It also updated the three starter tests to unpack the `(outcome, message)` tuple that `check_guess` is documented to return, instead of changing the function to match them. Bug 3 (New Game does not reset status, score or history) is still open and marked with a `FIXME` in `app.py`.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

**Reruns and session state.** Streamlit re-runs the whole script from top to bottom every time you click a button or change a widget, so ordinary variables are created fresh on every click. `st.session_state` is like a dictionary that survives those reruns, so anything the game has to remember, such as the secret, the attempts, the score and the status, lives there. Each value is guarded with `if "secret" not in st.session_state` so it is only set the first time, which is why the secret does not change on every click. Because the script runs in order, the Developer Debug Info panel prints before the Submit logic runs, so it showed the previous attempt count and history until the next rerun, which confused me at first.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

**A habit to reuse.** Write the failing test first and watch it fail before changing the code. The starter tests only checked the outcome label, so they stayed green while the hints lied, and seeing my new tests go red then green showed that they were actually testing the bug.

**What I would do differently.** I would start a fresh chat for each bug and read each file's diff as the assistant produces it, instead of reviewing everything at the end. I also want to ask the assistant to explain why a bug happens before it edits anything, so I am not just accepting a patch.

**How my view of AI generated code changed.** AI generated code can look tidy and come with passing tests and still be wrong, like the `except TypeError` fallback that quietly hid a real bug. I now treat it as a draft I have to verify myself, not as a finished result.
