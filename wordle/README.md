# Word Matching

## Setup and Usage
This project requires Python 3 (tested on Python 3.8) and NumPy. Please ensure you have these installed in your environment before trying to run this.

1. Run `match_word.py`
2. You will get a word suggestion. Try it.
3. Wordle will return values to you. _Correct letters in the **correct** position_ (i.e. <b style="color:green">green</b> in Wordle) translate to `+`. _Correct letters in the **wrong** position_ (i.e. <b style="color:yellow">yellow</b> in Wordle) translate to `~`. _Incorrect letters_ (i.e. <b style="color:grey">grey</b> in Wordle) translate to `-`.
4. Enter your sequence of `+`, `~`, and `-` in one line into the terminal (e.g. `++-~-`). Hit `Return`/`Enter`.
5. Repeat

## Licensing

The list of words is from [this link](https://github.com/dwyl/english-words/blob/master/words_alpha.txt) using the Unlicense as of 2022 Janurary 28.

## Notes
1. It does not get every word in the dictionary in 6 guesses.
2. A possible improvement would be to add a penalty for guessing duplicate letters.
  * UPDATE: I added a massive, unreasonably large penalty, but I am still working on this change. An important note is that currently, I "punish" duplicate answers equally hard, which is silly.
    * E.g. "sassy" should be penalized for a triple 's' more strongly than "sanes" is for a double 's'.
    * E.g. "abuzz" should be penalized for a double 'z' more strongly than "sanes" is for a double 's'.
3. ~I have never played Wordle, rather I am just guessing what the rules are based on what my colleague (June Cai) told me. Specifically, I do not know how duplicate letters in the wrong position are dealt with.~
  * ~E.g. Key word is "knoll"~
    * ~Guess: "level". Is the reply "\~---+"?~
    * ~Guess: "lilly". Is the reply "\~-\~+-" or "\~--+-"~
      * ~(i.e. only 1 of the L's in the wrong place is marked as belonging in the word)?~
      * ~Note that I defaulted to the former for ease of implementation.~
      * UPDATE: I looked it up and according to [this blog post](https://nerdschalk.com/wordle-same-letter-twice-rules-explained-how-does-it-work/), Wordle will mark excess letters as non-members (i.e. '-')
4. This game would be best solved by a decision tree using information entropy (I believe). I am not smart enough to that, so I have created this heuristic solver. Yay! (Just kidding, I wrote one in ROB311 but it was really hard and I don't want to think that hard again).
  * UPDATE: This may not be optimal for all scenarios. There is a trade-off between trying to guess the word in as few tries as possible ("greedy" or "exploitative") and trying to ensure that one does not need more than 6 guesses ("epsilon" or "exploratory").
6. I selected an arbitrary dictionary. This was not selected for any reason besides it being one of the first hits on Google. Wordle may full well use a different dictionary. I think this dictionary also includes plurals, so who knows?
7. ~I sum the unnormalized probabilities rather than multiplying them. This means that I do not use the probability. Also, because I used fixed-width integers (due to the NumPy array), you can get overflow. Maybe I should use the log-probability.~
  * UPDATE: This is fixed.

## Solution Explanations

### Heuristic Solutions

#### Independent Letter Probability Solver

This is the current implementation of the solver.

1. We generate a dictionary of possible 5-letter words
2. We find the probability of each of the 26 letters being in each of the 5 positions.
3. We select the word that has the greatest probability of each of its letters being in a given position.
  * This assumes that the probability of each letter being in a position is independent. Obviously it is not, because we have more common 2-letter combinations (e.g. "ee" is more common than "xq")
4. We use the feedback to remove the impossible words. (NOTE: this is mechanical and can be done perfectly assuming we have no mistakes).

### Information Entropy Solver

These are just some cursory notes on how I would go about solving this using information entropy. I do not guarantee correctness of this discussion; I have been using "information entropy" as a buzzword until now, so I will stop using this term in favour of _information gain_, in otherwords, how many options we have eliminated. That is, we wish to eliminate as many words as possible. I believe this solution will be much more computationally intensive than the previous.

An open question is whether the locally optimal solution (i.e. the guess that will eliminate the most words in the next round) the globally optimal solution (i.e. the branch of the decision tree it leads us down is has _both_ the fewest average steps to each leaf and the ). In other words, is the problem solveable with a greedy solver?

For every guess, we should calculate the gain from the guess and the opportunity cost. The gain is the number of possibilities that we can eliminate. This gives a computationally infeasible, but certainly correct solution (assuming the greedy solution is the globally optimal solution-- i.e. optimal substructure).

I thought that I showed optimal substructure between guesses too. However, I have heard of people creating solvers that look ahead. Maybe I made a mistake in my reasoning. I have not made a "formal proof" because I'm not a mathematical genius. But here is an outline:

> Let _dictionary_ be the original set of words.
> Let _wordA(\*)_ be the new set of possible words after filtering the words
> in \* that do not fit with the information we learned from guessing _wordA_.

> We will show the commutative property between guesses.
> Say that _wordA_ and then _wordB_ are two different words belonging to _dictionary_.
> The sets _wordA(wordB(dictionary))_ and _wordB(wordA(dictionary))_ are equal
> because they are equal to _wordA(dictionary)_ INTERSECTION _wordB(dictionary)_ 
> (**insert hand waving here**). 

> <=> the hint you get after guessing a word can be discarded after applying
> that filter to the set (all members fit this; none fits it 'more' than any other).

> => the state we end up in from guessing _wordA_ and then _wordB_ is 
> the same state as when we guess _wordB_ and then _wordA_.

> <=> the order of guesses is commutative. QED (well not really)

> Now, we will "prove" optimal substructure. Say _wordA(wordB(dictionary))_
> is the optimal solution. Therefore, if we choose _wordB_ first, we want to show
> that _wordA_ would be the best second choice. Now, assume toward a contraction that
> there exists a solution, _wordB(wordX(dictionary))_, which is a better choice,
> where _wordX_ =/= _wordA_. Now, using the commuative property, we rearrange it as
> _wordX(wordB(dictionary))_. And hence _wordX_ =/= _wordA_, and yet _wordA_ is any
> arbitrary word that will yield the optimal solution. This is a contradiction,
> hence we have optimal substructure.

> I apologize to my many talented mathematics teachers/professors for creating
> such a vague, hand-wavy, and likely holey proof. Also I apologize for abuses of notation.

```
let num_guesses: int = 6
let dictionary: set = all_candidate_words

for i in num_guesses:
  for key_word in dictionary:
    # This is a 'constraint' solver-- we are solving for what is possible rather than what is likely
    # We could construct a Bayesian probability solver by keeping track of the probability that each word is the key_word and factoring that into the decision
    # This would also be an iterative solver, making the problem even more immense
    let new_dictionary: dict[str -> set] = {word: set() for word in dictionary}

    # '-' denotes the difference of two sets
    for guess_word in dictionary - {key_word}:
      # |= is the union-equals operator. (a |= b) <=> (a = a UNION b)
      new_dictionary[guess_word] |= filter_out_impossible_words(answer=key_word, guess=word)

  pick_the_guess_word_with_smallest_number_of_possible_words(new_dictionary)


```

```
let num_guesses: int = 6
let dictionary: set = all_candidate_words

for i in num_guesses:
  for key_word in dictionary:
    # This is a 'constraint' solver-- we are solving for what is possible rather than what is likely
    # We could construct a Bayesian probability solver by keeping track of the probability that each word is the key_word and factoring that into the decision
    # This would also be an iterative solver, making the problem even more immense
    let new_dictionary: dict[str -> dict[str -> int]] = 0

    # '-' denotes the difference of two sets
    for guess_word in dictionary - {key_word}:
      # |= is the union-equals operator. (a |= b) <=> (a = a UNION b)
      possible_words = filter_out_impossible_words(answer=key_word, guess=word)
      for word in possible_words:
        new_dictionary[guess_word][word] += 1

  pick_the_guess_word_with_smallest_number_of_possible_words(new_dictionary)


```

As you can see, this algorithm is already `O(N^3)` (the `filter_out_impossible_words()` function is at least `O(N)`)! And this assumes the greedy solution is correct. Think about the crazy amount of compute this requires.

An example of the information we gain from a guess, "sanes" tells use that:
1. There is 0, 1, or >2 's'
2. There is 0 or >1 'a'
3. There is 0 or >1 'n'
4. There is 0 or >1 'e'
5. Whether there is an 's', 'a', 'n', 'e', and 's' in their relative positions
