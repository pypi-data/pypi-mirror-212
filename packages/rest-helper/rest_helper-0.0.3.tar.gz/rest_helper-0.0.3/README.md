# Rest Helper


## Overview
My Python App is a command-line utility that can be used to parse .ini files. It is compatible with Python 2.7 or later and Python 3.6 or later.

## Installation
To install Rest Helper, you have two options depending on your Python version:

### Python 3
`pip install -c constraints.txt .`


### Python 2
`python2 setup.py install`


## Usage
You can run My Python App with the following command-line options:
`python3 my_app.py -c <config_file> -n <number>`

### Options:
```
- `-c`, `--config`: Specifies the path to the configuration file (usually in .ini format).
- `-n`, `--num`: Specifies the number of lines to be printed.
- `-h`, `--help`: Show help message
```
### Example:
`python3 entrypoint.py -c config.ini -n 10`
