import math
import unittest
import fermat


class MyTestCase(unittest.TestCase):
    def testModExp(self):
        # Test for y = 0
        self.assertEqual(fermat.mod_exp(1, 0, 3), 1)
        # Test for z = 52
        self.assertEqual(fermat.mod_exp(11, 13, 53), 52)
        # Test for z = 3
        self.assertEqual(fermat.mod_exp(3, 8, 6), 3)

    def test_fermat(self):
        # Test for a known composite
        self.assertEqual(fermat.fermat(10, 3), 'composite')
        # Test for a known prime
        self.assertEqual(fermat.fermat(2621, 2000), 'prime')
        # Test for a known Carmichael number
        self.assertEqual(fermat.fermat(561, 560), 'composite')

    def test_millerRabin(self):
        # Test for a known composite
        self.assertEqual(fermat.miller_rabin(10, 3), 'composite')
        # Test for a known prime
        self.assertEqual(fermat.miller_rabin(2621, 2000), 'prime')
        # Test for a known Carmichael number
        self.assertEqual(fermat.miller_rabin(561, 560), 'composite')

    def testFProbability(self):
        # Test for small number
        self.assertEqual(fermat.fprobability(3), 0.125)
        # Test for a large number
        self.assertEqual(fermat.fprobability(560), 1 - 1 / math.pow(2, 560))

    def testMProbability(self):
        # Test for small number
        self.assertEqual(fermat.mprobability(3), 1 - 1 / 64)
        # Test for a large number
        self.assertEqual(fermat.mprobability(128), 1 / math.pow(4, 128))


if __name__ == '__main__':
    unittest.main()
