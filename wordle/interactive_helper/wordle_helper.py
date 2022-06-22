"""
################################################################################
Instructions
============

Installation (Unix-like only)
-----------------------------
1. Copy all the files in this directory (run.sh, dictionary.txt, and
wordle_helper.py). Do not change any file names (because I have hard-coded
these).
2. Ensure run.sh is an executable (`chmod +x run.sh`).

Running
-------
1. Go to the directory with these three files
1. Run with `./run.sh`.
2. Choose from the four functions 'grey', 'yellow', 'green' 
(note: case-sensitive!)
    * If one or more letters are grey, use `grey("<letters>")`,
    where <letters> are the grey letters.
        * You can see what letters are grey with `GREY`
    * If one or more letters are yellow for a given square, use
    `yellow(<square>, "<letters>")`, where <square> is the zero-indexed location
    and <letters> are the yellow letters.
        * You can see what letters are yellow with `YELLOW_REQUIRED`
        * You can see where the letters have been yellow with `YELLOW_EXCLUDE`
    * If a letter is green for a given square, use `green(<square>, "<char>")`,
    where <square> is the zero-indexed location and <char> is the character.
        * You can see what letters are green with GREEN
    * If you made a mistake or want to start again, use `reset()`.
        * And check that `ANS`, `GREY`, `YELLOW_EXCLUDE`, `YELLOW_REQUIRED`,
        and `GREEN` are reset.
TODO
====
1. Add LENGTH variable and allow for changing lengths (e.g. if we play hangman
or something)
"""

import os
from typing import List, Set, Tuple, Union


# These variables are important for functionality.
DICTIONARY_PATH: str = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "dictionary.txt",
)   # So we can have it on the interactive terminal.
ANS: List[str] = []

# These variables are not important for functionality.
# They are merely diagnostic tools.
GREY: Set[str] = set()
# Cannot multiply lists because then they are all the same object
YELLOW_EXCLUDE: Tuple[List, List, List, List, List] = tuple([] for _ in range(5))
YELLOW_REQUIRED: Set[str] = set()
GREEN: List[Union[str, None]] = [None] * 5


def reset():
    global GREY, YELLOW_EXCLUDE, YELLOW_REQUIRED, GREEN, ANS

    def get_five_letter_words():
        with open(DICTIONARY_PATH) as f:
            ans = [w for w in f.read().split("\n") if len(w) == 5]
        return ans

    GREY = set()
    YELLOW_EXCLUDE = tuple([] for _ in range(5))
    YELLOW_REQUIRED = set()
    GREEN = [None] * 5
    ANS = get_five_letter_words()
    return ANS


def grey(s: str):
    """Mark a string of (zero or more) letters as grey."""
    global GREY, ANS
    assert isinstance(s, str) and 0 < len(s)  and s.isalpha()

    lower_s = s.lower()
    GREY.update(c for c in lower_s)
    ANS = [w for w in ANS if all(map(lambda c: c not in w, lower_s))]
    return ANS


def yellow(idx: int, s: str):
    """Mark a string of (zero or more) letters as yellow in a position."""
    global YELLOW_EXCLUDE, YELLOW_REQUIRED, ANS
    assert isinstance(idx, int) and 0 <= idx <= 4
    assert isinstance(s, str) and s.isalpha()

    lower_s = s.lower()
    for c in lower_s:
        YELLOW_EXCLUDE[idx].append(c)
        YELLOW_REQUIRED.update(c)
        ANS = [w for w in ANS if w[idx] != c and c in w]
    return ANS


def green(idx: int, c: str):
    """Mark a single character as green in a position."""
    global GREEN, ANS
    assert isinstance(idx, int) and 0 <= idx <= 4
    assert isinstance(c, str) and len(c) == 1 and c.isalpha()
    assert GREEN[idx] is None

    lower_c = c.lower()
    GREEN[idx] = lower_c
    ANS = [w for w in ANS if w[idx] == lower_c] 
    return ANS


if __name__ == "__main__":
    ANS = reset()
