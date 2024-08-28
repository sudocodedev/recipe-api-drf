from django.test import SimpleTestCase
from app import calc

class CalcTests(SimpleTestCase):
    """
    Unit Test for calc module
    """

    def test_add_numbers(self):
        tc1=[3,4]
        tc2=['a',4]

        res1 = calc.add(tc1[0], tc1[1])
        res2 = calc.add(tc2[0], tc2[1])

        self.assertEqual(res1, 7)
        self.assertEqual(res2, 'Invalid inputs passed')

    def test_subtract_numbers(self):
        tc1=[3,4]
        tc2=['a',4]
        tc3=[5,4]
        
        res1 = calc.subtract(tc1[0], tc1[1])
        res2 = calc.subtract(tc2[0], tc2[1])
        res3 = calc.subtract(tc3[0], tc3[1])

        self.assertEqual(res1, -1)
        self.assertEqual(res2, 'Invalid inputs passed')
        self.assertEqual(res3, 1)
