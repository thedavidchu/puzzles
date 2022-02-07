# Word Matching

## Setup and Usage
This project requires Python 3 (tested on Python 3.8) and NumPy. Please ensure you have these installed in your environment before trying to run this.

1. Run `match_word.py`
2. You will get a word suggestion. Try it.
3. Wordle will return values to you. _Correct letters in the **correct** position_ (i.e. <b style="color:green">green</b> in Wordle) translate to `+`. _Correct letters in the **wrong** position_ (i.e. <b style="color:yellow">yellow</b> in Wordle) translate to `~`. _Incorrect letters_ (i.e. <b style="color:grey">grey</b> in Wordle) translate to `-`.
4. Enter your sequence of `+`, `~`, and `-` in one line into the terminal (e.g. `++-~-`). Hit `Return`/`Enter`.
5. Repeat

## Licensing

The list of words is from https://github.com/dwyl/english-words/blob/master/words_alpha.txt, using the Unlicense as of 2022 Janurary 28.

## Notes
1. It does not get every word in the dictionary in 6 guesses.
2. A possible improvement would be to add a penalty for guessing duplicate letters.
3. I have never played Wordle, rather I am just guessing what the rules are based on what my colleague (June Cai) told me. Specifically, I do not know how duplicate letters in the wrong position are dealt with.
  * E.g. Key word is "knoll"
    * Guess: "level". Is the reply "\~---+"?
    * Guess: "lilly". Is the reply "\~-\~+-" or "\~--+-"
      * (i.e. only 1 of the L's in the wrong place is marked as belonging in the word)?
      * Note that I defaulted to the former for ease of implementation.
      * UPDATE: I looked it up and according to [this blog post](https://nerdschalk.com/wordle-same-letter-twice-rules-explained-how-does-it-work/), Wordle will mark excess letters as non-members (i.e. '-')
4. This game would be best solved by a decision tree using information entropy (I believe). I am not smart enough to that, so I have created this heuristic solver. Yay! (Just kidding, I wrote one in ROB311 but it was really hard and I don't want to think that hard again).
  * UPDATE: This may not be optimal for all scenarios. There is a trade-off between trying to guess the word in as few tries as possible ("greedy" or "exploitative") and trying to ensure that one does not need more than 6 guesses ("epsilon" or "exploratory").
6. I selected an arbitrary dictionary. This was not selected for any reason besides it being one of the first hits on Google. Wordle may full well use a different dictionary. I think this dictionary also includes plurals, so who knows?
7. I sum the unnormalized probabilities rather than multiplying them. This means that I do not use the probability. Also, because I used fixed-width integers (due to the NumPy array), you can get overflow. Maybe I should use the log-probability.
