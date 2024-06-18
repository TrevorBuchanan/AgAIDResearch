import unittest

import numpy as np

from Helpers.utility import shuffle_in_unison


class MyTestCase(unittest.TestCase):
    def test_shuffle_in_unison(self):
        a = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        b = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        a_shuffled, b_shuffled = shuffle_in_unison(a, b)
        self.assertTrue(np.array_equal(a_shuffled, b_shuffled))


if __name__ == '__main__':
    unittest.main()
