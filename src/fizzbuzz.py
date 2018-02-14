class FizzBuzz:
    def do_it(self, value):
        if self._is_divisible_by_3(value) and self._is_divisible_by_5(value):
            return 'fizzbuzz'
        if self._is_divisible_by_3(value):
            return 'fizz'
        if self._is_divisible_by_5(value):
            return 'buzz'
        return value

    def _is_divisible_by_3(self, value):
        return value % 3 == 0

    def _is_divisible_by_5(self, value):
        return value % 5 == 0
