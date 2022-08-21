"""Functions used while determining text statistics (text_stats())"""
KEEP = {
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "n",
    "m",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    " ",
    "-",
    "'",
    "\n",
}


def normalize(s: str) -> str:
    """Normalize a given string"""

    return "".join((char for char in s.lower() if char in KEEP))


def number_of_words(s: str, unique=False) -> int:
    """Count number of words, unique or non-unique."""
    s = normalize(s)
    if unique is True:
        return len(set(s.split()))

    return len(s.split())


def number_of_characters(s: str, whitespace=False) -> int:
    """Count number of characters with or without whitespace."""

    if whitespace is True:
        return len(s)

    return len("".join(s.split()))


def number_of_lines(s: str) -> int:
    """Counts number of lines using built-in count() function"""

    return s.count("\n") + 1
