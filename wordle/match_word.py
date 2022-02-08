#!/bin/python3

import random
import re
from typing import Dict, List, Set, Tuple

import numpy as np


DICTIONARY_PATH: str = "words_length_5.txt"
WORD_LENGTH: int = 5
NUM_GUESSES: int = 6


def guess_word(text_words: List[str], word_length: int, explore: bool):
    if not text_words:
        raise ValueError("No more words to choose from!")
    
    # Step 1: Process words (convert to lowercase), convert to number from 0..=25)
    def word_to_int_seq(word: str) -> Tuple[int, ...]:
        assert word.isalpha()
        return tuple(ord(l) - ord("a") for l in word.lower())

    words = np.array([word_to_int_seq(word) for word in text_words])
    num_words = len(words)

    # Step 2: Find the frequency of each letter appearing in each position
    hist = np.zeros((26, word_length))
    for j, col in enumerate(words.T):
        hist[:, j], _ = np.histogram(col, 26, (0, 26))

    # Step 3: Find the probability of each letter appearing in its place
    # NOTE: the "probability" should be normalized by dividing by the number of words
    prob_letters = np.zeros_like(words)
    for j, col in enumerate(words.T):
        prob_letters[:, j] = np.take(hist[:, j], col)
    prob_letters = np.log(prob_letters / num_words)

    # Step 4: Find the probability of each word
    prob_words = np.sum(prob_letters, axis=1)
    
    # Step 5: If explore, do not guess duplicates. Else, pick the best
    if explore:
        max_prob = np.max(prob_words)
        all_unique = np.array(tuple(map(lambda word: len(np.unique(word)) == word_length, words)))
        prob_words = np.where(
            all_unique,
            prob_words,
            prob_words + max_prob
        )
    # Step b: Find the most likely word
    def int_seq_to_word(seq: Tuple[int, ...]) -> str:
        return "".join(chr(s + ord("a")) for s in seq)

    most_likely_idx = np.argmax(prob_words)
    most_likely_word = int_seq_to_word(words[most_likely_idx])
    return most_likely_word


def update_pattern(old_pattern: List[Set[str]], old_required: str, guess: str, reply: str):
    """
    Note: we apply the filter every time, so we don't need to check for the old pattern/old requirements.


    old_pattern: list[set[str]]
        The possible characters for each position in the word. E.g. [{"a", "b"}, {"c", "d", "e"}]
    old_required: str
        A string of characters that are required to be present in the string.
    guess: str
        The latest guess. E.g. "hello".
    reply: str
        The reply stating the status of each character.
    """
    new_pattern = old_pattern
    new_required = ""
    for i, char in enumerate(guess):
        # Correct letter, correct position
        if reply[i] == "+":
            new_pattern[i] = {char}
            new_required += char
        # Correct letter, wrong position
        elif reply[i] == "~":
            new_pattern[i] -= {char}
            new_required += char
        # Wrong letter, wrong position
        elif reply[i] == "-":
            # Not duplicate letter
            if char not in new_required:
                new_pattern = [
                    p - {char} for p in new_pattern
                ]
            # Duplicate letter
            else:
                new_pattern[i] -= {char}
        else:
            raise ValueError("unexpected value in reply")

    # Combine old_required and new_required
    if old_required:
        for i, char in enumerate(old_required):
            num_in_old = old_required.count(char)
            num_in_new = new_required.count(char)
            if num_in_old > num_in_new:
                new_required += char * (num_in_old - num_in_new)
    return new_pattern, new_required


def apply_filter(words: List[str], pattern: List[Set[str]], required: str):
    re_pattern = f"[{']['.join(''.join(p) for p in pattern)}]"
    r = re.compile(re_pattern)
    # Remove words that don't fit the pattern
    words: iter = filter(r.match, words)
    # Remove words without the required letters
    words: list = [w for w in words if all(w.count(req) >= required.count(req) for req in required)]
    return words


def test_word(key: str, guess: str):
    if not all(map(lambda var: isinstance(var, str), [key, guess])):
        raise TypeError("invalid types, expecting strings")
    elif len(key) != len(guess):
        raise ValueError("invalid lengths, key and guess are different lengths")

    def create_multiset(key: str) -> Dict[str, int]:
        return {c: key.count(c) for c in key}

    reply_list = [None] * WORD_LENGTH
    multiset = create_multiset(key)
    for i, char in enumerate(guess):
        if key[i] == char:
            reply_list[i] = "+"
            multiset[char] -= 1
    
    for i, char in enumerate(guess):
        if reply_list[i] is not None:
            continue
        # If the char is in the key and we are expecting 1 or more of it
        # NOTE: the dict lookup is valid bc the first statement will short-circuit
        # if it is false.
        elif char in key and multiset[char]:
            reply_list[i] = "~"
            multiset[char] -= 1
        else:
            reply_list[i] = "-"

    if not all(map(lambda count: count >= 0, multiset.values())):
        raise ValueError("too many of one character have been used")

    return "".join(reply_list)


################################################################################


def test(num: int = None):
    # Load key words
    with open(DICTIONARY_PATH) as f:
        all_text_words = f.read().split("\n")
    
    test_words_list = (
        all_text_words 
        if num is None
        else random.sample(all_text_words, k=num)
    )
    num_words = len(test_words_list)

    # Compute Score
    score = 0
    total_guesses = 0
    for i, key_word in enumerate(test_words_list):
        r = test_key_word(key_word)
        if r:
            score += 1
            total_guesses += r
        else:
            total_guesses += NUM_GUESSES

    print(f"Score: {score}/{num_words} = {score / num_words if num_words else None}")
    print(f"Total Guesses: {total_guesses}/{num_words * NUM_GUESSES} = {total_guesses / (num_words * NUM_GUESSES) if num_words and NUM_GUESSES else None}")


def test_key_word(key_word: str) -> int:
    # Step 1: Load words (separated by "\n")
    with open(DICTIONARY_PATH) as f:
        all_text_words = f.read().split("\n")

    print(f"Word: {key_word}")
    # Step 2: Major Filters (length, ascii)
    filtered_text_words = [word for word in all_text_words if len(word) == WORD_LENGTH and word.isalpha()]

    # Step 3: Set up for repeated guessing
    text_words = filtered_text_words    # Reset every iteration
    pattern = [{l for l in "abcdefghijklmnopqrstuvwxyz"} for _ in range(WORD_LENGTH)]
    required = ""
    for i in range(NUM_GUESSES):
        # Step 4: Guess most likely word
        most_likely_word = guess_word(text_words, WORD_LENGTH, explore=(i < NUM_GUESSES - 1))
        print(f"\tGuess: {most_likely_word}")
        reply = test_word(key_word, most_likely_word)
        if "-" not in reply and "~" not in reply:
            break
        # Step 5: Filter words based on reply and repeat
        pattern, required = update_pattern(pattern, required, most_likely_word, reply)
        text_words = apply_filter(text_words, pattern, required)
    else:
        print(f"YOU FAILED ON {key_word}!")
        return 0
    print("SUCCESS!")
    return i + 1


################################################################################


def main():
    # Step 1: Load words (separated by "\n")
    with open(DICTIONARY_PATH) as f:
        all_text_words = f.read().split("\n")

    # Step 2: Major Filters (length, ascii)
    filtered_text_words = [word for word in all_text_words if len(word) == WORD_LENGTH and word.isalpha()]

    # Step 3: Set up for repeated guessing
    text_words = filtered_text_words    # Reset every iteration
    pattern = [{l for l in "abcdefghijklmnopqrstuvwxyz"} for _ in range(WORD_LENGTH)]
    required = ""
    for i in range(NUM_GUESSES):
        # Step 4: Guess most likely word
        most_likely_word = guess_word(text_words, WORD_LENGTH, explore=(i < NUM_GUESSES - 1))
        print(f"Guess {i + 1}: {most_likely_word}")
        
        reply = input("What is the reply? (Type 'help' for instructions): ")
        while reply == "help" or len(reply) != WORD_LENGTH or not all(map(lambda c: c in "+~-", reply)):
            print()
            print("Instructions")
            print("============")
            print(f"Enter a {WORD_LENGTH} character string using the characters {{'+', '~', '-'}} where")
            print("    '+' implies correct letter and position,")
            print("    '~' means correct letter but wrong position, and")
            print("    '-' means neither correct letter nor correct position.")
            print("Note that if the keyword is 'knoll' but you were to guess 'lilly', the response would be '~-~+-' because it does not count the number of correct letters")
            print()
            reply = input("What is the reply? (Type 'help' for instructions)")

        if reply == "+" * WORD_LENGTH:
            break
        # Step 5: Filter words based on reply and repeat
        pattern, required = update_pattern(pattern, required, most_likely_word, reply)
        text_words = apply_filter(text_words, pattern, required)
    else:
        print(f"YOU FAILED ON MYSTERY WORD!")
        return False
    print("SUCCESS!")
    return True
    

if __name__ == "__main__":
    # main()
    # test(50)
    test_key_word("gazer")
    r = input("PRESS ANY KEY TO CONTINUE")
