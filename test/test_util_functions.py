import unittest

from rst_link_checker import checkline


class TestUtils(unittest.TestCase):

    def test_checkline_fails_with_no_argument(self):
        self.assertTrue(checkline('a'))


if __name__ == '__main__':
    unittest.main()
