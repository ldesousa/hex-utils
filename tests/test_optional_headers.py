'''
Created on Mar 31, 2018

@author: duque004
'''

import unittest
from hex_utils.hasc import HASC

class OptionalHeadersTest(unittest.TestCase):
    
    def setUp(self):
        
        self.h = HASC()
    
    def testMissingAngle(self):
        
        self.h.loadFromFile("../data/test02.hasc")
        self.assertEqual(self.h.get(0,0), float(23), "The first cell value read from test02.hasc is not 23.")
        
    def testMissingEmpty(self):
        
        self.h.loadFromFile("../data/test03.hasc")
        self.assertEqual(self.h.get(0,0), float(23), "The first cell value read from test03.hasc is not 23.")
        
    def testMissingAngleEmpty(self):
        
        self.h.loadFromFile("../data/test04.hasc")
        self.assertEqual(self.h.get(0,0), float(23), "The first cell value read from test04.hasc is not 23.")
   
        
def load_tests(loader=None, tests=None, pattern=None):
    """Load local tests
    """
    if not loader:
        loader = unittest.TestLoader()
    suite_list = [
        loader.loadTestsFromTestCase(OptionalHeadersTest)
    ]
    return unittest.TestSuite(suite_list)
        