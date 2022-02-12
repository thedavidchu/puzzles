"""
# Hang Man Player

This is a REPL hangman player. Hangman is a game where there is a secret
word that one tries to guess. Every incorrect word is placed and a "body
part" of the person to be hanged is drawn (a rather gruesome game, but
not my idea). If the full person is drawn, the guesser loses; if not,
then they win. The number of body parts to be drawn varies between
players.


## Hangman Instructions

1. Nominate someone to pick a SECRET WORD. We will call this person the
   CHOOSER. Everyone else will try to guess the word; they will be known
   collectively as the GUESSERS.
2. The CHOOSER tells the GUESSERS how many letters are in the SECRET
   WORD in the form of underscores. For example, a five letter word is
   denoted:

       - - - - -
3. The GUESSERS guess letters. If the letter belongs in the word, the
   CHOOSER will place the letter above on of the dashed lines:

         E
       - - - - -
   Otherwise, the letter is placed next to the gallows and a part of the
   hanged man is drawn.
     _____
     |   |   A B C D
     |   O
     |  -|-
     |
   __|__

4. This process continues until either (a) the whole word is guessed or
   (b) the entire hangman is drawn. The number of guesses allotted to
   the GUESSERS should be known a priori.


## Implementation Details

This is a very basic solution. It does not say any words are more likely
than others. That is, it treats the probability of each word as equally
likely until it is proven otherwise regardless of the probability of a
word appearing in the English language.

The dictionary I have selected is from [this link]
(https://github.com/dwyl/english-words/blob/master/words_alpha.txt)
using the Unlicense on 2022 Janurary 28.

WARNING: I have not tested this.


## Note on the Language

The name "hangman" is in keeping with [this Wikipedia article]
(https://en.wikipedia.org/wiki/Hangman_(game))as of the time of this
writing. This happens to be the most commonly used name, which is why
such a macabre image is evoked. Furthermore, this code is not actively
maintained. Nothing in this project condones violence or capital
punishment.
"""

import re
from typing import List


class HangMan:
    def __init__(self, dictionary_path: str):
        self.dictionary_path: str = dictionary_path
        self.dictionary: List[str] = self.get_dictionary(self.dictionary_path)
        self.word_length: int = None

    @staticmethod
    def get_dictionary(dictionary_path: str):
        """Get words from a dictionary file, where words are separated by new lines."""
        with open(dictionary_path) as f:
            dictionary = [
                word.lower()
                for word in f.read().split("\n")
                if word.isascii()
            ]
        return dictionary

    def refresh(self):
        # Refresh the dictionary and restore all words
        self.dictionary = self.get_dictionary(self.dictionary_path)

    ####
    #   INFO
    ####

    def status(self):
        # Print the number of words left in the dictionary
        print(f"({len(self.dictionary)})")


    def display(self):
        # Print the list of words in the dictionary
        print(f"({len(self.dictionary)}) {self.dictionary}")

    ####
    #   FILTER
    ####

    def length(self, length: int):
        # Filter words that do not have the specified length
        self.word_length = length
        self.dictionary = list(filter(lambda word: len(word) == length, self.dictionary))

    def no(self, char: str):
        # Filter words containing letters in the input
        for c in char:
            self.dictionary = list(
                filter(lambda word: c not in word, self.dictionary)
            )

    def match(self, filter_: str):
        # Match words that fit this regex input
        r = re.compile(filter_)
        self.dictionary = list(filter(r.match, self.dictionary))

    ####
    #   GUESS
    ####
    
    def guess(self):
        abc = "abcdefghijklmnopqrstuvwxyz"
        letters = {l: 0 for l in abc}
        for word in self.dictionary:
            for l in abc:
                if l in word:
                    letters[l] += 1
        argmax = "a"
        for l in abc:
            if letters[l] > letters[argmax]:
                argmax = l
        print(f"Guess: {l}")


def help_():
    print()
    print("Help")
    print("====")
    print("Print any part of the beginning of a command. We will match the rest for you (if it is ambiguous, it will pick the first option)")
    print()
    print("Commands")
    print("--------")
    print()
    print("refresh (): refresh the word list. This takes no arguments")
    print("length (int): remove all words that do not have the specified length")
    print("no (str): remove all words containing letters in the specified string")
    print("match (str): remove all words that do not match the specified regex filter")
    print("status : print the number of possibilities")
    print("display : print the possibilities")
    print("guess : print the best letter (i.e. occurs in the most words)")
    print("help/anything else : print this help menu!")
    print("exit : exit the game")
    print("***")
    print("E.g. `>>> len 10` filters all words that do not have 10 letters.")
    print()
    print()


def main():
    h = HangMan(".\words.txt")
    while h.dictionary:       
        reply = input(">>> ")

        cmd, *args = reply.split(' ')

        # Check whether the reply matches the first part of
        # the function name
        match_fn = lambda fn: re.match(
            f"{cmd}.*",
            fn.__name__
        )

        # If no reply, continue to next iteration
        if not reply:
            continue
        # Exit if asked
        elif reply == "exit":
            break
        # Refresh
        elif match_fn(h.refresh):
            if args:
                print("refresh takes no arguments")
                help_()
            else:
                h.refresh()
        # Info
        elif match_fn(h.status):
            if args:
                print("status takes no arguments")
                help_()
            else:
                h.status()
        elif match_fn(h.display):
            if args:
                print("display takes no arguments")
                help_()
            else:
                h.display()
        # Filter
        elif match_fn(h.length):
            if len(args) != 1:
                print("length takes one argument")
                help_()
            else:
                try:
                    h.length(int(*args))
                except ValueError:
                    print("length takes an integer argument")
                    help_() 
        elif match_fn(h.no):
            if len(args) != 1:
                print("no takes one argument")
                help_()
            else:
                h.no(*args)
        elif match_fn(h.match):
            if len(args) != 1:
                print("match takes one argument")
                help_()
            else:
                try:
                    h.match(*args)
                except:
                    print("match takes a valid regex string")
                    help_()
        # Guess
        elif match_fn(h.guess):
            if args:
                print("guess takes no arguments")
                help_()
            else:
                h.display()

        else:
            help_()


if __name__ == "__main__":
    main()
