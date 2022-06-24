# Puzzles
Playing with cryptography, steganography (stenography is the short-hand), and other encoding tools.

## steganography

I use this script:

```bash
# in this current directory
python steganography \
    --visible-path .images/Forests.jpg \
    --hidden-path .images/wildfire_768_60.jpg \
    --steganograph-path .images/steganograph.png; # note: it has to be a png so the lesser-significant pixels do not get messed up.
```

to take my outwardly visible image:

![Serene Forest](https://github.com/thedavidchu/puzzles/blob/main/.images/Forests.jpg?raw=true)

and hide this image in the lesser-visible bits of the pixels:

![Forest Fire](https://github.com/thedavidchu/puzzles/blob/main/.images/wildfire_768_60.jpg?raw=true)

to get:

![Steganograph](https://github.com/thedavidchu/puzzles/blob/main/.images/steganograph.png?raw=true)

Note the drop in quality, because the lower pixels are used to disguise the hidden image.

## wordle

The interactive Wordle assistant uses human input and returns possible output words.

![Wordle state after two guesses](https://github.com/thedavidchu/puzzles/blob/main/.images/wordleguess2-2022-06-23.png?raw=true)

The output of the interactive Wordle assistant:

![Wordle state after two guesses](https://github.com/thedavidchu/puzzles/blob/main/.images/wordlesolver-guess2-2022-06-23.png?raw=true)

## TODO
- Upload pretty pictures of the steganography
- Show the self-replicating source code in a demo

