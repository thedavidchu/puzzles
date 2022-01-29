# Word Matching

## Licensing

List of words is from https://github.com/dwyl/english-words/blob/master/words_alpha.txt, using the Unlicense as of 2022-01-28.

## Notes
1. It does not get every word in the dictionary in 6 guesses.
2. A possible improvement would be to add a penalty for guessing duplicate letters
3. I have never played Wordle, rather I am just guessing what the rules are based on what my colleague (June Cai) told me. Specifically, I do not know how duplicate letters in the wrong position are dealt with.
  * E.g. Key word is "knoll"
    * Guess: "level". Is the reply "\~---+"?
    * Guess: "lilly". Is the reply "\~-\~+-" or "\~--+-"
      * (i.e. only 1 of the L's in the wrong place is marked as belonging in the word)?
  * Note that I defaulted to the former for ease of implementation.
4. This game would be best solved by a decision tree using information entropy. I am not smart enough to that, so I have created this heuristic solver. Yay! (Just kidding, I wrote one in ROB311 but it was really hard and I don't want to think that hard again)
5. I used a random dictionary. This was not selected for any reason besides it being one of the first hits on Google. Wordle may full well use a different dictionary. I think this dictionary also includes plurals, so who knows?