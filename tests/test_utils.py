import unittest
from app.utils import sanitize


class TestSanitize(unittest.TestCase):
    def setUp(self):
        self.invalid_chars = ["\n", "\r", "\t", "<", ">", "%s", ";", "/", "(", ")", "\u202e", "\x00"]
        self.base_string = "Hello{}World"
        self.pattern = "[^\w \d\"#\$%&'\(\)\*\+,-\.\/:;?@\^_`{\|}~]+|\%\w+|;|/|\(|\)"

    def test_sanitize_invalid_characters(self):
        for char in self.invalid_chars:
            test_string = self.base_string.format(char)
            with self.subTest(char=char):
                sanitized = sanitize(test_string, self.pattern)
                self.assertNotIn(char, sanitized, f"Invalid character '{char}' was not removed")


if __name__ == "__main__":
    unittest.main()
