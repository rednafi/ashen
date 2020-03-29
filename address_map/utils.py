import re
import string


def clean_term(term, join_delimiter, add_fuzzy=False):

    # lower
    term = term.lower()

    # remove numbers
    term = re.sub(r"[^a-zA-Z]", " ", term)

    # remove punctuations
    table = str.maketrans({key: None for key in string.punctuation})
    term = term.translate(table)

    # remove pre-post spaces
    term = term.strip()

    # split by space
    term = re.findall(r"\S+", term)

    # eliminate words with length < 3
    term = [w for w in term if len(w) > 3]

    if add_fuzzy:
        # Append suffix / prefix to strings in list
        term = ["%" + sub + "%" for sub in term]

    # join by delimiter
    term = join_delimiter.join(term)

    return term
