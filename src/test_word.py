import unittest
from word import *

class TestWord(unittest.TestCase):
    def test_next(self):
        n = Word("next")
        w = Word("word", None, next=n)
        self.assertEqual(w._next, n)
        self.assertEqual(w._next._text, n._text)

    def test_update_backspace_with_no_entry1(self):
        p = Word("prev")
        w = Word("word", p)
        w.is_current = True
        r = w.update("", is_backspace=True)
        self.assertEqual(w.is_current, False)
        self.assertEqual(p.is_current, True)
        self.assertEqual(r, p)

    def test_update_backspace_with_no_entry2(self):
        w = Word("word")
        w.is_current = True
        r = w.update("", is_backspace=True)
        self.assertEqual(w.is_current, True)
        self.assertEqual(r, w)

    def test_update_history(self):
        w = Word("word")
        w.is_current = True
        w.update("f")
        w.update("o")
        w.update("o")
        r = w.update("", is_backspace=True)
        self.assertEqual(w._entered_history, ["f", "o"])
        self.assertEqual(w._full_entered_history, ["f", "o", "o"])

    def test_update_space1(self):
        n = Word("next")
        w = Word("word", None, next=n)
        w.is_current = True
        r = w.update(" ")
        self.assertEqual(w.is_current, False)
        self.assertEqual(n.is_current, True)
        self.assertEqual(r, n)

    def test_update_space2(self):
        w = Word("word")
        w.is_current = True
        r = w.update(" ")
        self.assertEqual(w.is_current, True)
        self.assertEqual(r, w)

    def test_update_max_entries(self):
        w = Word("x")
        w.is_current = True
        w.update("a")
        w.update("a")
        w.update("a")
        w.update("a")
        w.update("a")
        w.update("a")
        self.assertEqual(['a', 'a', 'a', 'a', 'a'], w._entered_history)
        self.assertEqual(['a', 'a', 'a', 'a', 'a'], w._full_entered_history)


if __name__ == "__main__":
    unittest.main()