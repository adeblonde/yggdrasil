import unittest

class GlobalTest(unittest.TestCase) :

    """ Test case for first function """

    """ prepare setup """
    def setUp(self) :
        self.name = 'test'
    
    """ tear down """
    def tearDown(self) :
        self.name = None

    """ test writing to S3 """
    def test_write2s3(self) :
		self.name = 'test writing to S3'