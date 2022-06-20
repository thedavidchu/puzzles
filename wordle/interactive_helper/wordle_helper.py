import os
from typing import List, Set, Tuple, Union


# These variables are important for functionality.
THIS_FILE: str = __file__   # So we can have it on the interactive terminal.
ANS: List[str] = []

# These variables are not important for functionality. They are merely diagnostic tools.
GREY: Set[str] = set()
# Cannot multiply lists because then they are all the same object
YELLOW_EXCLUDE: Tuple[List, List, List, List, List] = tuple([] for _ in range(5))
YELLOW_REQUIRED: Set[str] = set()
GREEN: List[Union[str, None]] = [None] * 5


def reset():
    global GREY, YELLOW_EXCLUDE, YELLOW_REQUIRED, GREEN, ANS

    def get_five_letter_words():
        dictionary_path: str = os.path.join(
            os.path.dirname(os.path.abspath(THIS_FILE)), 
            "dictionary.txt"
        )
        with open(dictionary_path) as f:
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
    assert isinstance(s, str) and 0 < len(s) 

    GREY.update(c for c in s)
    ANS = [w for w in ANS if all(map(lambda x: x not in w, s))]
    return ANS


def yellow(idx: int, s: str):
    """Mark a string of (zero or more) letters as yellow in a given position."""
    global YELLOW_EXCLUDE, YELLOW_REQUIRED, ANS
    assert isinstance(idx, int) and 0 <= idx <= 4
    assert isinstance(s, str) and s.isalpha()

    for c in s:
        YELLOW_EXCLUDE[idx].append(c.lower())
        YELLOW_REQUIRED.update(c)
        ANS = [w for w in ANS if w[idx] != c and c in w]
    return ANS


def green(idx: int, c: str):
    """Mark a single character as green in a given position."""
    global GREEN, ANS
    assert isinstance(idx, int) and 0 <= idx <= 4
    assert isinstance(c, str) and len(c) == 1 and c.isalpha()
    assert GREEN[idx] == None

    GREEN[idx] = c
    ANS = [w for w in ANS if w[idx] == c] 
    return ANS


if __name__ == "__main__":
    ANS = reset()
