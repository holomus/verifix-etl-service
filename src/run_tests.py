import unittest
from tests import TestSmartupExtractionClient

def suite():
  suite = unittest.TestSuite()
  suite.addTest(TestSmartupExtractionClient('test_extraction'))
  return suite

if __name__ == '__main__':
  runner = unittest.TextTestRunner()
  runner.run(suite())