from unittest import TestCase

from textarium.text import Text

class TestText(TestCase):
    def test_prepare_0(self):
        input_text = """
        Hello! My name is Mr.Parker.
        I have a website https://parker.com.
        It has about 5000 visitors per day.
        I track it with a simple html-block like this:
        <div>Google.Analytics</div>
        """
        expected_result = (
            "hello my name is mr parker"\
            " i have a website it has about visitors per day"\
            " i track it with a simple html block like this"\
            " google analytics"
        )
        text = Text(input_text)
        text.prepare()
        self.assertEqual(expected_result, text.prepared_text)