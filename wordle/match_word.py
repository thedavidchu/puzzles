#!/bin/python3
import re
from typing import List, Set, Tuple

import numpy as np


def guess_word(text_words: List[str], word_length: int):
    # Step 3: Process words (convert to lowercase), convert to number from 0..=25)
    def word_to_int_seq(word: str) -> Tuple[int, ...]:
        assert word.isalpha()
        return tuple(ord(l) - ord("a") for l in word.lower())


    words = np.array([word_to_int_seq(word) for word in text_words])

    # Step 4: Find the frequency of each letter appearing in each position
    hist = np.zeros((26, word_length))
    for j, col in enumerate(words.T):
        hist[:, j], _ = np.histogram(col, 26, (0, 26))

    # Step 5: Find the probability of each letter appearing in its place
    # NOTE: the "probability" should be normalized by dividing by the number of words
    prob_letters = np.zeros_like(words)
    for j, col in enumerate(words.T):
        prob_letters[:, j] = np.take(hist[:, j], col)

    # Step 6: Find the probability of each word
    prob_words = np.sum(prob_letters, axis=1)

    # Step 7: Find the most likely word
    def int_seq_to_word(seq: Tuple[int, ...]) -> str:
        return "".join(chr(s + ord("a")) for s in seq)


    most_likely_idx = np.argmax(prob_words)
    most_likely_word = int_seq_to_word(words[most_likely_idx])
    return most_likely_word


def update_pattern(old_pattern: List[Set[str]], old_required: str, guess: str, reply: str):
    """
    Note: we apply the filter every time, so we don't need to check for the old pattern/old requirements

    old_pattern: list[set[str]]
        The possible characters for each position in the word. E.g. [{"a", "b"}, {"c", "d", "e"}]
    old_required: str
        A string of characters that are required to be present in the string.
    guess: str
        The latest guess. E.g. "hello"
    reply: str
        The reply stating the 
    """
    new_pattern = old_pattern
    new_required = old_required
    for i, position in enumerate(old_pattern):
        # Correct letter, correct position
        if reply[i] == "+":
            new_pattern[i] = {guess[i]}
        # Correct letter, wrong position
        elif reply[i] == "~":
            new_pattern[i] -= {guess[i]}
            new_required += guess[i]
        # Wrong letter, wrong position
        elif reply[i] == "-":
            new_pattern = [
                p - {guess[i]} for p in new_pattern
            ]
        else:
            raise ValueError("unexpected value in reply")
    return new_pattern, new_required
            

def apply_filter(words: List[str], pattern: List[Set[str]], required: str):
    re_pattern = f"[{']['.join(''.join(p) for p in pattern)}]"
    r = re.compile(re_pattern)
    # Remove words that don't fit the pattern
    words: iter = filter(r.match, words)
    # Remove words without the required letters
    words: list = [w for w in words if all(req in w for req in required)]
    return words


def test_word(key: str, guess: str):
    if not all(map(lambda var: isinstance(var, str), [key, guess])):
        raise TypeError("invalid types, expecting strings")
    elif len(key) != len(guess):
        raise ValueError("invalid lengths, key and guess are different lengths")

    reply_list = []
    for i, char in enumerate(guess):
        if key[i] == guess[i]:
            reply_list.append("+")
        elif guess[i] in key:
            reply_list.append("~")
        else:
            reply_list.append("-")

    return "".join(reply_list)


def test():
    KEY_WORD = "knoll"
    DICTIONARY_PATH = "words_length_5.txt"
    WORD_LENGTH = 5
    
    # Step 1: Load words (separated by "\n")
    with open(DICTIONARY_PATH) as f:
        all_text_words = f.read().split("\n")

    # Step 2: Major Filters (length, ascii)
    filtered_text_words = [word for word in all_text_words if len(word) == WORD_LENGTH and word.isalpha()]

    # Step 3: Set up for repeated guessing
    text_words = filtered_text_words    # Reset every iteration
    pattern = [{l for l in "abcdefghijklmnopqrstuvwxyz"} for _ in range(WORD_LENGTH)]
    required = ""
    for i in range(6):
        # Step 4: Guess most likely word
        most_likely_word = guess_word(text_words, WORD_LENGTH)
        print(f"\tGuess: {most_likely_word}")
        reply = test_word(KEY_WORD, most_likely_word)
        if "-" not in reply and "~" not in reply:
            break
        # Step 5: Filter words based on reply and repeat
        pattern, required = update_pattern(pattern, required, most_likely_word, reply)
        text_words = apply_filter(text_words, pattern, required)
    else:
        print(f"YOU FAILED ON {KEY_WORD}!")
        return False
    print("SUCCESS!")
    return True


def main():
    DICTIONARY_PATH = "words_length_5.txt"
    WORD_LENGTH = 5

    # Step 1: Load words (separated by "\n")
    with open(DICTIONARY_PATH) as f:
        all_text_words = f.read().split("\n")

    # Step 2: Major Filters (length, ascii)
    filtered_text_words = [word for word in all_text_words if len(word) == WORD_LENGTH and word.isalpha()]

    # Step 3: Set up for repeated guessing
    text_words = filtered_text_words    # Reset every iteration
    pattern = [{l for l in "abcdefghijklmnopqrstuvwxyz"} for _ in range(WORD_LENGTH)]
    required = ""
    for i in range(6):
        # Step 4: Guess most likely word
        most_likely_word = guess_word(text_words, WORD_LENGTH)
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
        print(f"YOU FAILED ON {KEY_WORD}!")
        return False
    print("SUCCESS!")
    return True
    


if __name__ == "__main__":
    main()
    r = input("PRESS ANY KEY TO CONTINUE")
