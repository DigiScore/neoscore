import unittest

from brown.tools import pitch_tools
from brown.exceptions import IncompatibleValuesError

class TestPitchTools(unittest.TestCase):


    def test_find_pitch_class_calculates_correctly_with_positive_value(self):
        self.assertEqual(pitch_tools.find_pitch_class(23), 11)

    def test_find_pitch_class_calculates_correctly_with_negative_value(self):
        self.assertEqual(pitch_tools.find_pitch_class(-23), 1)

    def test_find_pitch_class_raises_ValueError_with_bad_value(self):
        self.assertRaises(ValueError, pitch_tools.find_pitch_class, 'non int-convertible str')

    def test_find_octave_with_pitch_num_only(self):
        self.assertEqual(pitch_tools.find_octave(24), 2)
        self.assertEqual(pitch_tools.find_octave(12), 1)
        self.assertEqual(pitch_tools.find_octave(10), 0)
        self.assertEqual(pitch_tools.find_octave(0), 0)
        self.assertEqual(pitch_tools.find_octave(-10), -1)
        self.assertEqual(pitch_tools.find_octave(-12), -1)
        self.assertEqual(pitch_tools.find_octave(-24), -2)

    def test_find_octave_with_pitch_num_and_letter(self):
        self.assertEqual(pitch_tools.find_octave(12, 'c'), 1)
        self.assertEqual(pitch_tools.find_octave(10, 'b'), 0)
        self.assertEqual(pitch_tools.find_octave(0, 'c'), 0)
        self.assertEqual(pitch_tools.find_octave(-10, 'd'), -1)
        self.assertEqual(pitch_tools.find_octave(-12, 'c'), -1)
        self.assertEqual(pitch_tools.find_octave(-24, 'c'), -2)

    def test_find_octave_with_pitch_num_and_letter_edge_cases(self):

        # B-sharp should not be the same octave as C-natural on the same pitch number
        self.assertEqual(pitch_tools.find_octave(24, 'b'), 1)
        # Similarly, C-flat should not be the same octave as B-natural on the same pitch number
        self.assertEqual(pitch_tools.find_octave(11, 'c'), 1)



if __name__ == '__main__':
    unittest.main()
