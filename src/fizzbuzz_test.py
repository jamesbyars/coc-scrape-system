import unittest

from fizzbuzz import FizzBuzz


class FizzBuzzTest(unittest.TestCase):
    def setUp(self):
        self.app = FizzBuzz()

    def test_returns_one_when_one(self):
        self.assertEqual(self._submit_value(1), 1, "1 should return 1")

    def test_returns_fizz_when_three(self):
        self.assertEqual(self._submit_value(3), 'fizz')

    def test_returns_fizz_when_six(self):
        self.assertEqual(self._submit_value(6), 'fizz')

    def test_returns_buzz_when_five(self):
        self.assertEqual(self._submit_value(5), 'buzz')

    def test_returns_buzz_when_ten(self):
        self.assertEqual(self._submit_value(10), 'buzz')

    def test_returns_four_when_four(self):
        self.assertEqual(self._submit_value(4), 4)

    def test_returns_fizzbuzz_when_15(self):
        self.assertEqual(self._submit_value(15), 'fizzbuzz')

    def _submit_value(self, value):
        return self.app.do_it(value=value)


if __name__ == '__main__':
    unittest.main()
