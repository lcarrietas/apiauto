import unittest


class TestProject(unittest.TestCase):

    # fixture
    def setUp(self):
         """
        Test Setup
        """
        print("Setup")

    def test_one(self):
         """
        Test one
        """
        print("test one")

    def test_two(self):
         """
        Test two
        """
        print("test two")

    def test_three(self):
        print("test three")

    # fixture
    def tearDown(self):
         """
        Test three
        """
        print("tearDown")
