import json
import random
import re


class FileError(Exception):
    """A general class for file operation error"""

    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


def get_all_quotes():
    """It returns all quotes from quote.json."""
    data = {}
    try:
        f = open("quote.json", "r")
        data = json.load(f)
    except (FileNotFoundError, JSONDecodeError) as e:
        message = """File 'quote.json' not found, or not a json file,
Perhaps you forgot to scrape first"""
        raise FileError(message)

    quotes_list = []
    for topic in data["topics"]:
        quotes = list(topic.values())[0][1:]  # first item is omited
        quotes_list.extend(quotes)
    return quotes_list


def search_quote(kword):
    """It returns a list of quotes(person, quote), based on keyword,
    It assumes one keyword, which is trimmed."""
    result = []
    data = get_all_quotes()

    # del_re = re.compile(r'\w[\s]\w')
    for quo in data:
        if kword.lower() in list(re.split(r"\W", quo["quote"].lower())):
            result.append(quo)

    return result


def get_random_item(q_list):
    """It returns a quote, from a list of quotes."""
    sample = random.choice(q_list)
    return sample
