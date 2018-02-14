## Now test it

from services import FakeDataService

import unittest


class TestDataService(unittest.TestCase):

    def setUp(self):
        self.service = FakeDataService()

    def test_read(self):
        self.assertEqual('fake read data', self.service.read_data())


if __name__ == '__main__':
    unittest.main()