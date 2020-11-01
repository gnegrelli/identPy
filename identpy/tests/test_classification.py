import unittest
import numpy as np

from identpy.methods.parameter_classification import velez_reyes


class TestClassification(unittest.TestCase):

    def test_velez_reyes(self):
        cases = [
            (np.array([[144.9, 325.5],
                      [325.5, 5298.1]]),
             [0, 1]),
            (np.array(
                [[373578, -75959, 107886, -911851, -4372, 9, -576],
                 [-75959, 15598, -22258, 189047, 902, -2, 117],
                 [107886, -22258, 33476, -298238, -1392, 9, -163],
                 [-911851, 189047, -298238, 2772982, 12640, -183, 1348],
                 [-4372, 902, -1392, 12640, 59, 0.18, 6],
                 [9, -2, 9, -183, 0.18, 0.93, 0],
                 [-576, 117, -163, 1348, 6, 0, 0.93]]),
             [0, 3, 1, 2, 4, 5, 6]),
        ]

        for case, result in cases:
            self.assertListEqual(result, list(velez_reyes(case)))


if __name__ == '__main__':
    unittest.main()
