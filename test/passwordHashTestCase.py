import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
import efc_v3

class PasswordHashTestCase(unittest.TestCase):
    
    def setUp(self):
        self.password = 'passwd-123-$pecia1'
        self.blank_password = ''

    """        we can't test the hash itself, just checking the output length and correct format. """

    def test_add_pepper_valid_for_password(self):
        # we can't test the hash itself, just checking the output length and correct format.
        hash = efc_v3.add_pepper(self.password)
        self.assertEqual(len(hash), 60, 'incorrect hash')

    """        we can't test the hash itself, just checking the output type """

    def test_add_pepper_invalid_for_password(self):
        hash = efc_v3.add_pepper(self.blank_password)
        self.assertEqual(None, hash, 'incorrect hash')


if __name__ == "__main__":
    unittest.main()
