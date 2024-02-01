import unittest
from state_sight import state_sight
import datetime
import numpy as np


class TestStateSightDecorator(unittest.TestCase):

    def test_state_sight_logging(self):
        # Arrange: Create a class with the decorator
        @state_sight(log_file='test_log.json', buffer_size=20)
        class TestClass:

            def __init__(self):
                self.x = 0
                self.y = 0

        # Act: Create an object and change its state
        obj = TestClass()
        obj.x = 1
        obj.x = 2

        # Assert: Check if the log contains the expected entries
        log = obj.get_log()
        self.assertEqual(len(log), 3)
        self.assertEqual(log[1]['Change']['previous'], 0)
        self.assertEqual(log[1]['Change']['current'], 1)
        self.assertEqual(log[2]['Change']['previous'], 1)
        self.assertEqual(log[2]['Change']['current'], 2)

    def test_state_sight_customization(self):
        # Arrange: Create a class with customized logging settings
        @state_sight(buffer_size=100,
                     log_lists=True,
                     log_dicts=True,
                     log_numpy_arrays=True)
        class CustomClass:

            def __init__(self, my_list=None, my_dict=None):
                self.my_list = my_list
                self.my_dict = my_dict

        # Act: Create an object and change its state
        obj = CustomClass(my_list=[1, 2, 3], my_dict={"key": "value"})
        obj.my_list = [4, 5, 6]
        obj.my_dict = {"key": "value", "new_key": "new_value"}

        # Assert: Check if the log contains the expected entries
        log = obj.get_log()
        self.assertEqual(len(log), 3)
        self.assertEqual(log[0]['Change'], "Initial State")
        self.assertEqual(log[1]['Change']['current'], [4, 5, 6])
        self.assertEqual(log[1]['Change']['previous'], [1, 2, 3])
        self.assertEqual(log[2]['Change']['current'], {
            "key": "value",
            "new_key": "new_value"
        })


if __name__ == '__main__':
    unittest.main()
