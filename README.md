# StateSight
StateSight is a Python package that brings transparency to your Python class state changes. Designed to provide runtime insights for the python classes, StateSight empowers developers to observe, track, and understand changes within their objects (class), making debugging and data analysis more intuitive than ever.

## Key Features
- **Real-Time State Logging:** StateSight keeps a detailed log of all state changes in your Python classes, providing a historical record of modifications.
- **Customizable Logging:** Choose to log specific types of data such as lists, dictionaries, numpy arrays, or any combination thereof.
- **File Output Flexibility:** Log data can be outputted to various file formats including JSON, CSV, and TXT.
- **Buffer Size Management:** Control the memory footprint by setting the buffer size, ensuring efficient usage even in memory-intensive applications.
- **Seamless Integration:** StateSight integrates effortlessly with existing Python classes using a simple decorator, requiring minimal code changes.
- **Class-Specific Logging:** StateSight allows you to have separate loggers for different classes, making it easier to track and analyze state changes in distinct parts of your codebase.

### Installation
Clone the repository from GitHub to start using StateSight in your project:

```bash
git clone https://github.com/yourusername/StateSight.git
```

## Quick Start
Enhance your class with StateSight in just a few lines:

```python
from statesight import state_sight

@state_sight(buffer_size = 100, log_file='state_log.json')
class MyClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Instantiate your class and see StateSight in action
my_object = MyClass(1, 'initial state')
my_object.x = 2  # This change will be logged by StateSight

print(my_object.get_log())
```
**Output**

```bash
[{'Timestamp': '2024-02-01T17:15:28.272609', 'Changed Attribute': 'x', 'Change': {'previous': None, 'current': 1}, 'State': {'x': 1}}, {'Timestamp': '2024-02-01T17:15:28.273616', 'Changed Attribute': 'y', 'Change': {'previous': None, 'current': 'initial state'}, 'State': {'x': 1, 'y': 'initial state'}}, {'Timestamp': '2024-02-01T17:15:28.273616', 'Changed Attribute': '', 'Change': 'Initial State', 'State': {'x': 1, 'y': 'initial state'}}, {'Timestamp': '2024-02-01T17:15:28.274524', 'Changed Attribute': 'x', 'Change': {'previous': 1, 'current': 2}, 'State': {'x': 2, 'y': 'initial state'}}]
```

## Advanced Example
For a more in-depth demonstration of StateSight's capabilities, consider the following advanced use case. This example showcases StateSight's ability to handle a variety of data types including numpy arrays, lists, dictionaries, and even custom functions.

```python
from state_sight import state_sight
import numpy as np
import datetime

# Example class to demonstrate advanced StateSight features
@state_sight(buffer_size=5, log_file='log.json', log_lists=True, log_dicts=True, log_numpy_arrays=True)
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

if __name__ == "__main__":
    # Instantiate the class and perform various operations
    obj = MyClass(10, 'Hello')
    obj.x = 20
    obj.y = 'World'
    obj.array = np.array([4, 5, 6])
    obj.dict_example = {"new_key": "new_value"}
    obj.list_example = [4, 5, 6]
    obj.some_thing = datetime.datetime.now()
    obj.some_thing = say_hello()
    obj.some_thing = say_hello

    # Output the serialized current state and the complete change log
    print(obj.to_json())  # Serializes current state to JSON
    print(obj.get_log())  # Retrieves the log of all changes
```
In this example, modifications to different types of attributes are logged, demonstrating StateSight's versatility. The logged information is invaluable for debugging and understanding the object's state transitions over time.

## Contributing
Contributions are what make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

## License
StateSight is made available under the MIT License. See the LICENSE file for more details.

## Contact
Feel free to reach out in Issues for any questions or suggestions.
