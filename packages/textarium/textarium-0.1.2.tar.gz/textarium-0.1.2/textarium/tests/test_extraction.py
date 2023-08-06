from unittest import TestCase

import textarium.extraction as extraction

class TestExtraction(TestCase):
    def test_extract_words_en_0(self):
        test_input = "This line has 5 tokens"
        expected_result = ["This", "line", "has", "5", "tokens"]
        result = extraction.extract_words(test_input)
        self.assertEqual(expected_result, result)

    def test_extract_words_ru_0(self):
        test_input = "В этой строке 5 токенов"
        expected_result = ["В", "этой", "строке", "5", "токенов"]
        result = extraction.extract_words(test_input)
        self.assertEqual(expected_result, result)

    def test_extract_sentences_en_0(self):
        text_input = """
        Hello! My name is Robbie. 
        Please, write an email to Mr. Parker. 
        His email: parker@gmail.com.
        """
        expected_result = [
            "Hello!", "My name is Robbie.", 
            "Please, write an email to Mr. Parker.", 
            "His email: parker@gmail.com."
        ]
        result = extraction.extract_sentences(text_input, lang='en')
        self.assertEqual(expected_result, result)

    def test_extract_sentences_ru_0(self):
        text_input = """
        Привет! Меня зовут Робби.
        Пожалуйста, напиши письмо (т. е. e-mail) Паркеру.
        Его адрес: parker@gmail.com.
        """
        expected_result = [
            "Привет!", "Меня зовут Робби.",
            "Пожалуйста, напиши письмо (т. е. e-mail) Паркеру.",
            "Его адрес: parker@gmail.com."
        ]
        result = extraction.extract_sentences(text_input, lang='ru')
        self.assertEqual(expected_result, result)

    def test_extract_urls_0(self):
        text_input = """
        There is one link: http://google.com.
        And another one: https://www.google.com/images?v=1&p=2!
        This is not a link: test@gmail.com
        """
        exptected_result = [
            "http://google.com",
            "https://www.google.com/images?v=1&p=2"
        ]
        result = extraction.extract_urls(text_input)
        self.assertEqual(exptected_result, result)
