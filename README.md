# crapgrep

Have you ever wanted to use a poorly-written, less-featured, slower replacement for an existing [powerful tool?](https://www.gnu.org/software/grep/)

Then this is for you...

## What is this?

`crapgrep` is a poor imitation of the Unix utility `grep` written in Python.  
More specifically, it's a command line tool to search for a pattern or a substring in each line of one or more text files.

The command synopsis is very similar to `grep`, although it needs the Python interpreter to be invoked explicitly (at the moment, at least):

```
python crapgrep.py [OPTIONS] [PATTERN] [FILE[...]]
```

_**Note**: obviously, `crapgrep` doesn't read from `stdin`, which makes it even more useless..._

## Examples

The examples below assume that `python` is an alias of `python3`.

### Simple search

Searching for the simple string `'hola'` in file `garbage.txt` in the current directory:

```
python crapgrep.py hola garbage.txt
```

To make the search case-insensitive, you could do:

```
python crapgrep.py -i hOlA garbage.txt
```

### Regexp

_**Note**: unlike `grep`, `crapgrep` doesn't treat the string as a regular expression pattern by default, it must be specified by passing the `-E` option explicitly._ 

Searching for pattern `'^urka[0-9]'` in files `garbage1.txt` and `garbage2.txt` in the parent directory:

```
python crapgrep.py -E '^urka[0-9]' ../garbage1.txt ../garbage2.txt
```

When multiple files are passed, `crapgrep` will prepend the file name to the matched lines printed to `stdout`.

Considering the example above, the output could be something like:

```
../garbage1.txt:urka2 paletta
../garbage2.txt:urka4l8
```

### Line numbers

Passing the `-n` option will cause line numbers to be prepended, so adding `-n` to the regexp example:

```
python crapgrep.py -E -n '^urka[0-9]' ../garbage1.txt ../garbage2.txt
```

could output something like:

```
../garbage1.txt:5:urka2 paletta
../garbage2.txt:73:urka4l8
```

meaning that the matches were found in lines `5` and `73` of `garbage1.txt` and `garbage2.txt`, respectively.

## Test coverage

Ehm...

## Why

If you're asking yourself: "_Why would you inflict something like this upon the world?_", the answer is... because it's fun!

## TODO

- [ ] Implement the recursive search option (`-r`)
- [ ] Implement long options (e.g.,`--ignore-case`)
- [ ] Abandon the project!!
