import unittest
import logging
import whcfix.utils as utils
import whcfix.settings as settings


class UtilsTests(unittest.TestCase):

    def test_nz_swaps_none_with_empty_string(self):
        @utils.nz
        def function_that_returns_None():
            return None
        expected = ""
        actual = function_that_returns_None()
        self.assertEqual(expected, actual)

    def test_nz_returns_results_that_are_not_None(self):
        @utils.nz
        def function_that_returns_foo():
            return "foo"
        expected = "foo"
        actual = function_that_returns_foo()
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format=settings.LOG_FORMAT)
    unittest.main()
