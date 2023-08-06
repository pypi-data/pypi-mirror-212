# -*- coding: utf-8 -*-

"""
Corpus class.
"""
from typing import List
from .text import Text

class Corpus:
    def __init__(self, texts: List[str], lang='en'):
        self.lang = lang
        self.corpus = [Text(t, lang=self.lang) for t in texts]

    def __str__(self):
        first_five_texts = "\n\n".join([t.raw_text for t in self.corpus[:5]])
        last_five_texts = "\n\n".join([t.raw_text for t in self.corpus[-5:]])
        return first_five_texts + "\n\n...\n\n" + last_five_texts

    def __repr__(self):
        return f"textarium.Corpus object containing {len(self.corpus)} textarium.Text objects"

    def prepare(self, lemmatize: bool = True, stopwords: List[str] = None):
        for t in self.corpus:
            t.prepare(lemmatize=lemmatize, stopwords=stopwords)