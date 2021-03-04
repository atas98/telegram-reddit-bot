import unittest
from reddit import _subreddit_is_valid

class TestStringMethods(unittest.TestCase):

    def test_invalid(self):
        self.assertEqual(_subreddit_is_valid("\./12313\./"), "")
        self.assertEqual(_subreddit_is_valid("@somestring"), "")
        self.assertEqual(_subreddit_is_valid(""), "")

    def test_valid_without_prefix(self):
        self.assertEqual(_subreddit_is_valid("all"),         "all")
        self.assertEqual(_subreddit_is_valid("programming"), "programming")
        self.assertEqual(_subreddit_is_valid("learnpython"), "learnpython")
        
    def test_valid_with_prefix(self):
        self.assertEqual(_subreddit_is_valid("r/all"), "all")
        self.assertEqual(_subreddit_is_valid("r/programming"), "programming")
        self.assertEqual(_subreddit_is_valid("r/learnpython"), "learnpython")



if __name__ == '__main__':
    unittest.main()