# Reflections on Trusting Trust

After reading Ken Thompson's article entitled "Reflections on Trusting Trust",
I decided to take a crack at creating a program that self-replicates its source
code.

Two key observations allowed me to do this:
1. printf's format is not applied recursively
2. printf allows one to easily duplicate strings in the 

The file `trojan.c` is more of a proof-of-concept rather than anything
malicious, especially considering it only prints to the stdout. But it was an
interesting exercise.
