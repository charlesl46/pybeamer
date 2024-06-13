import string
import random

from tests.test_case import PyBeamerTestCase

from pybeamer.utils import math,italic

class TestUtils(PyBeamerTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.text = "".join(random.choices(list(string.ascii_letters),k=random.randint(0,100)))

    def test_math(self):
        text_math = math(self.text)
        self.assertEqual(text_math,f"${{{self.text}}}$")

    def test_italic(self):
        text_italic = italic(self.text)
        self.assertEqual(text_italic,r"\textit{%s}" % self.text)