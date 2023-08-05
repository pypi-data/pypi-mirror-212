# -*- coding: utf-8 -*-

"""
Function for extracting information from texts.
"""

import re
import string
from typing import List
from razdel import sentenize
from nltk import tokenize
import textarium.preprocessing as preprocessing

def extract_words(text: str) -> List[str]:
    """Extract a list of tokens from a text

    Args:
        text (str): Any string

    Returns:
        List[str]: A list of extracted tokens
    """
    words = tokenize.word_tokenize(text)
    return words

def extract_sentences(text: str, lang='en') -> List[str]:
    """Extract a list of sentences from a text

    Args:
        text (str): Any string in English or Russian
        lang (str): Text language ('ru' - Russian or 'en' - English)

    Returns:
        List[str]: A list of extracted sentences
    """
    if lang == 'en':
        sentences = tokenize.sent_tokenize(text)
        sentences = [preprocessing.remove_extra_spaces(s) for s in sentences]
    elif lang == 'ru':
        sentences = [i.text for i in sentenize(text)]
    return sentences

def extract_urls(text:str) -> List[str]:
    """Extract a list of URLs from a text

    Args:
        text (str):Any string

    Returns:
        List[str]: A list of extracted URLs
    """
    url_regex = re.compile(
        "((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)", re.DOTALL
    )
    parsed_url_objects = re.findall(url_regex, text)
    urls = [url_param[0].strip(string.punctuation) for url_param in parsed_url_objects]
    return urls
