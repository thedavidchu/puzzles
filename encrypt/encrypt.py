"""
# Encrypt a message with XOR

## Purpose
You can encrypt files here! Yay. Only problem is that it is rather poor.

## Note
I did not test this code. Assume it does not work.
"""

import argparse

def get_file(file_name):
    with open(file_name, 'r') as f:
        file = f.read()

    return file


def write_file(file_name, text):
    with open(file_name, 'w') as f:
        file = f.write(text)

    return


def encrypt(whence, key):
    """
    Encrypt whence variable using key using bitwise XOR.
    Yes, I know this is the worse encryption possible, but still.
    I also know that putting it in the docstring means you can look it up.

    :param whence: the string that you wish to encrypt.
    :param key: the key that you want to use in the code.

    :return: either the encoded or decoded message.
    
    """
    # Process key
    if isinstance(key, int):
        key_ = [key]
    elif isinstance(key, str):
        key_ = [ord(i) for i in key]

    whither = ''

    for i, letter in enumerate(whence):
        whither += chr(key_[i % len(key_)] ^ ord(letter))

    return whither

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", type=str, required=True)
    parser.add_argument("--output-file", type=str, required=True)
    parser.add_argument("--key", type=str, required=True)
    args = parser.parse_args()
    
    a = get_file(args.input_file)
    key = args.key
    b = encrypt(a, key)
    write_file(args.output_file, b)
    
