# Plog

A package for logging data and objects in different steps of applications.


## How to use
Install the package. It is tested on Python **3.9+** 

````
pip install plog-python
````

## Directory Structure
````
plog
├── components
│   ├── checkpoint.py
│   ├── __init__.py
│   ├── objectframe.py
│   └── task.py
├── db
│   └── engine.py
├── handlers
│   ├── __init__.py
│   ├── log_handler.py
│   ├── object_handler.py
│   └── plog_handler.py
├── __init__.py
└── models
    ├── file_model.py
    ├── __init__.py
    └── log_model.py
````


## Modules

- **components**: Contains the component files for the project.
  - `checkpoint.py`: Defines the checkpoint component.
  - `objectframe.py`: Defines the object frame component.
  - `task.py`: Defines the task component.

- **db**: Includes the database related files.
  - `engine.py`: Handles the database engine and connection.

- **handlers**: Contains different handlers for various functionalities.
  - `log_handler.py`: Handles interactions with the log data.
  - `object_handler.py`: Handles interactions with the object data.
  - `plog_handler.py`: Handles the main functionality of the plog application.

- **models**: Includes the model files for the project.
  - `file_model.py`: Defines the file model used in log entries.
  - `log_model.py`: Defines the log model used for log entries.
