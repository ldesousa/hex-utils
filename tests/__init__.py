import sys
import unittest

from tests import test_optional_headers

def load_tests(loader=None, tests=None, pattern=None):
    """Load tests
    """
    return unittest.TestSuite([
        test_optional_headers.load_tests(),
    ])

if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(load_tests())
    if not result.wasSuccessful():
        sys.exit(1)