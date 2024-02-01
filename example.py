from state_sight import state_sight
import numpy as np
import datetime

if __name__ == "__main__":
    # Example Usage
    @state_sight(buffer_size=5,
                 log_file='log.json',
                 log_lists=True,
                 log_dicts=True,
                 log_numpy_arrays=True)
    class MyClass:

        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.array = np.array([1, 2, 3])
            self.dict_example = {"key": "value"}
            self.list_example = [1, 2, 3]
            self.some_thing = datetime.datetime.now()

    def say_hello():
        print("Hello")
        return "Hello"

    # Testing the logging
    obj = MyClass(10, 'Hello')
    obj.x = 20
    obj.y = 'World'
    obj.array = np.array([4, 5, 6])
    obj.dict_example = {"new_key": "new_value"}
    obj.list_example = [4, 5, 6]
    obj.some_thing = datetime.datetime.now()
    obj.some_thing = say_hello()
    obj.some_thing = say_hello

    print(obj.to_json())  # Serializes current state to JSON
    print(obj.get_log())  # Retrieves the log of all changes
