import json
import datetime
import os
import csv
import numpy as np


def state_sight(buffer_size: int = 100,
                log_file: str = None,
                log_lists: bool = False,
                log_dicts: bool = False,
                log_numpy_arrays: bool = False):
    """
    A decorator that adds state logging functionality to a class. It logs 
    changes in the class's attributes, including the initial state and 
    subsequent modifications. The logged data includes timestamps, the 
    attribute changed, its previous and current values, and the entire state 
    of the object.
    
    Args:
    buffer_size (int): The maximum number of changes to keep in memory. Default is 100.
    log_file (str): The file to log changes to. Can be a JSON, CSV or TXT file. 
                    Any other extension will be saved as txt format. If None, no file logging is done.
    log_lists (bool): Whether to log list objects. Default is False.
    log_dicts (bool): Whether to log dictionary objects. Default is False.
    log_numpy_arrays (bool): Whether to log numpy arrays. Default is False.
    
    Returns:
    cls: The class with the added state logging functionality.
    

    Usage:
    Decorate any class with @StateLogger to enable logging. For example:
    
    ```python
    @state_sight(log_file='log.json')
    class MyClass:
        def __init__(self, attr1, attr2):
            self.attr1 = attr1
            self.attr2 = attr2
    
    # trace the changes
    obj = MyClass(10, 'Hello')
    obj.attr1 = 20
    obj.attr2 = 'World'
    obj.attr1 = 30
    obj.attr2 = 'World'
    
    print(obj.to_json())  # Serializes current state to JSON    
    print(obj.get_log())  # Retrieves the log of all changes
    
    ```
    
    Once decorated, instances of the class will automatically log state changes.
    These logs can be accessed using the `get_log` method or saved to a file.
    """

    def decorator(cls):

        class LoggerWrapper(cls):
            _internal_attributes = {
                '_log', '_buffer_size', '_log_to_file', '_log_file',
                '_internal_attributes'
            }

            def __init__(self, *args, **kwargs):
                self._log = []
                self._buffer_size = buffer_size
                self._log_file = log_file
                super().__init__(*args, **kwargs)
                # reset the log after initialization
                self._log = []
                self._log_state("Initial State")

            def __setattr__(self, name, value):
                try:
                    prev_value = self._log[-1]['State'][
                        name] if self._log else None
                except:
                    prev_value = self.__dict__.get(name, None)
                object.__setattr__(self, name, value)

                if name not in self._internal_attributes:
                    simple_prev_value = self._simplify_value(prev_value)
                    simple_value = self._simplify_value(value)

                    change_msg = {
                        "previous": simple_prev_value,
                        "current": simple_value
                    }
                    self._log_state(change_msg, name)

            def _simplify_value(self, value):
                """ Simplify the value for logging """
                if isinstance(value, list) and not log_lists:
                    return '<list object>'
                elif isinstance(value, dict) and not log_dicts:
                    return '<dict object>'
                elif isinstance(value, np.ndarray) and not log_numpy_arrays:
                    return '<numpy array object>'
                else:
                    return value

            def _log_state(self, change_msg=None, changed_attr=""):
                """ Log the current state """
                state_snapshot = {
                    k: self._simplify_value(v)
                    for k, v in self.__dict__.items()
                    if k not in self._internal_attributes
                }
                timestamp = datetime.datetime.now().isoformat()
                log_entry = {
                    'Timestamp': timestamp,
                    'Changed Attribute': changed_attr,
                    'Change': change_msg,
                    'State': state_snapshot
                }
                # print(log_entry)
                self._log.append(log_entry)

                if len(self._log) > self._buffer_size:
                    self._log.pop(0)
                    print("Buffer full, removing oldest entry")

                if self._log_file:
                    self._write_log_to_file()

            def _write_log_to_file(self):
                """ Write the log to file in the appropriate format """
                file_ext = os.path.splitext(self._log_file)[1]
                if file_ext.lower() == '.json':
                    with open(self._log_file, 'w') as file:
                        json.dump(self._log,
                                  file,
                                  default=self._default_serializer,
                                  indent=4)
                elif file_ext.lower() == '.csv':
                    with open(self._log_file, 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([
                            'Timestamp', 'Changed Attribute', 'Change', 'State'
                        ])
                        for entry in self._log:
                            writer.writerow([
                                entry['Timestamp'], entry['Changed Attribute'],
                                json.dumps(entry['Change'],
                                           default=self._default_serializer),
                                json.dumps(entry['State'],
                                           default=self._default_serializer)
                            ])

                else:
                    with open(self._log_file, 'w') as file:
                        for entry in self._log:
                            json_entry = json.dumps(
                                entry, default=self._default_serializer)
                            # as string
                            json_entry = json_entry[1:
                                                    -1]  # remove curly braces
                            file.write(json_entry + '\n')

            def _default_serializer(self, obj):
                """ Custom serializer for JSON """
                try:
                    if isinstance(obj, np.ndarray) and log_numpy_arrays:
                        return obj.tolist()
                    return str(obj)
                except:
                    return type(obj)

            def get_log(self):
                """ Return the current log """
                return self._log

            def to_json(self):
                """ Serialize the current state to JSON """
                return json.dumps(self,
                                  default=self._default_serializer,
                                  sort_keys=False,
                                  indent=4)

        return LoggerWrapper

    return decorator


if __name__ == "__main__":
    # Example Usage
    @state_sight(buffer_size=50,
                 log_file='log.json',
                 log_lists=False,
                 log_dicts=True,
                 log_numpy_arrays=False)
    class MyClass:

        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.array = np.array([1, 2, 3])
            self.dict_example = {"key": "value"}
            self.list_example = [1, 2, 3]
            self.some_thing = datetime.datetime.now()

    def say_hello():
        return "Hello"

    # Testing the logging
    obj = MyClass(10, 'Hello')
    obj.dict_example['keyx'] = 'new_value'
    obj.x = 200
    obj.array = np.array([4, 5, 6])
    obj.y = 'World'
    obj.array = np.array([4, 5, 6])
    obj.dict_example = {"new_key": "new_value"}
    obj.list_example = [4, 5, 6]
    obj.some_thing = datetime.datetime.now()
    obj.some_thing = say_hello()
    obj.some_thing = say_hello

    print(obj.to_json())  # Serializes current state to JSON
    print(obj.get_log())  # Retrieves the log of all changes
