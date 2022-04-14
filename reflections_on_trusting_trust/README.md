# Reflections on Trusting Trust

After reading Ken Thompson's article entitled "Reflections on Trusting Trust",
I decided to take a crack at creating a program that self-replicates its source
code.

Two key observations allowed me to do this:
1. `printf`'s format is not applied recursively.
    * E.g. `printf("%s", "%s");` will print `%s`.
2. `printf` allows one to easily duplicate strings in the `stdout`.
    * E.g. `printf("%s%s", string, string);` will print `string` twice.

The file `generate_trojan.c` is more of a proof-of-concept rather than anything
of value, especially considering it only prints to the standard output; rather,
it was an interesting exercise. Also, similarly to Thompson's example file,
`generate_trojan.c` is not, strictly-speaking, self-replicating. However, it
does self-replicate its functionality.

The reason is that the file `generate_trojan.c` has pretty formatting (i.e.
indentation, new lines, and comments), for which I did not want to recreate the
self-replicating functionality. But the output from `generate_trojan.c`, located
in the file `trojan.c`, is truly self-replicating.

To check for whether a C file is self-replicating, run the following script:

```bash
# Compile and run the first file
gcc trojan.c
./a.out > resultA.c

# Compile and run the output file
gcc resultA.c
./a.out > resultB.c

# The compare function should print nothing if the files are identical.
cmp resultA.c resultB.c
```

There should be no standard output from the `cmp` function. This denotes
success.
