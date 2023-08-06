import unittest
from charred import is_same_char, is_unicode_char, repeat_char


class TestChar(unittest.TestCase):
    def test_is_same_char(self):
        self.assertEqual(is_same_char('FF'), True)
        self.assertEqual(is_same_char('FD'), False)

    def test_is_unicode_char(self):
        self.assertEqual(is_unicode_char('£'), True)
        self.assertEqual(is_unicode_char('F'), False)

    def test_char_repeat(self):
        self.assertEqual(repeat_char('F', 6), 'FFFFFF')


if __name__ == '__main__':
    unittest.main()
