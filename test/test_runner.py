import unittest
import test_encrypt
import test_decrypt
import passwordHashTestCase

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_encrypt))
suite.addTests(loader.loadTestsFromModule(test_decrypt))
suite.addTests(loader.loadTestsFromModule(passwordHashTestCase))

# initialize a runner and run
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
