import unittest
import logging


class Tests(unittest.TestCase):

    def test_main(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()