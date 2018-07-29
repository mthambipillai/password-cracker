# password-cracker
Basic password cracker as a proof-of-concept for educational purposes. Given a hash and a cracking technique, the program applies the technique to recover the original password from the hash. This project is intended as a learning material for my [video](#) about password cracking on my [Youtube channel](https://www.youtube.com/channel/UCMzZh0q-rcd9yDEOTXAH90g).

## Requirements

You need to have [Python](https://www.python.org/downloads/) installed to run the script.

## Usage

You can run the password cracker with the command `python password_cracker.py`. It takes two positional arguments : the hash to crack and the attack to run. It takes different optional arguments depending on the attack chosen. You can find all parameters with `python password_cracker.py --help`

Possible attacks are :
- `brute_force` : Tries all possible alphanumerical passwords with length smaller or equal to `--length_max`.
- `dict` : Tries all passwords contained in a dictionary file provided by `--dictionary`.
- `dict_repl` : Tries all passwords contained in a dictionary file provided by `--dictionary` and for each password it tries passwords obtained by replacements given by `--replacements`. A replacement replaces all occurences of the old char by the new char in the password.
- `targeted` : Tries all possible permutations of all possible subsets of a list of words given by `--words`.

## Contributing

There is no license (see UNLICENSE.txt) so feel free to clone the project and make improvements, there are so many that you can try to implement!