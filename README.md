# Demandator  [![version](https://img.shields.io/badge/version-1.0.0-green.svg)]()

Demandator is a package to use to ask image classification of images from your shell.

### Features
- Classify images
- Plot graph of prediction
- Save results to improve the AI model throught transfer learning 
- Manage users 



### Gettin' Started

Demandator requires [Python](https://www.python.org/downloads/release/python-360/) 3.6 to run.

Download the package and install the dependencies.

**1) Open folder in terminal**
**2) Create a new user with the following command**
```bash
$ python demandator_pkg/scripts/dbmanager.py -a <name_user> -p <password>
```
**3) Test the program with one the images provided**
```bash
$ python main.py test_images/test.jpg -p <password> -u <username>
```
**4) If everything worked properly (🤞) you can run the classificator with your own files**
```bash
$ python main.py <image-path> -p <password> -u <username>
```

### Optional Arguments
You can add one or more of the below arguments to personalize your queries

| Arg | DFLT | Range | Description |
| ------ | ------ | ------ | ------ |
| -g | off | None | Plot the graph of predictions |
| -n | 5 | 1-50 | Number of results to display |
| -v | off | count <= 2 | Display verbosity |
| -t | 0.0 | 0 <= Float <= 1  | Limit results to that minimum threshold |


### Technologies
Demandator is created with:
- [Python 3.6](https://www.python.org/downloads/release/python-360/)

### Modules
Demandator uses a number of modules to work properly, so make sure to have them properly installed:

* [numpy](https://pypi.org/project/numpy/) - NumPy is the fundamental package for scientific computing with Python
* [argparse](https://docs.python.org/3/library/argparse.html) - Parser for command-line options, arguments and sub-commands
* [hashlib](https://docs.python.org/3/library/hashlib.html) - Secure hashes and message digests
* [sqlite3](https://docs.python.org/2/library/sqlite3.html) - DB-API 2.0 interface for SQLite databases
* [os](https://docs.python.org/3/library/os.html) - Miscellaneous operating system interfaces
* [sys](https://docs.python.org/3/library/sys.html) - System-specific parameters and functions
* [requests](https://pypi.org/project/requests/) - Python HTTP for Humans.
* [ast](https://docs.python.org/3/library/ast.html) - Abstract Syntax Trees
* [PIL](https://pypi.org/project/Pillow/) - Python Imaging Library
* [cv2](https://pypi.org/project/opencv-python/) - Wrapper package for OpenCV python bindings.
* [logging](https://docs.python.org/2/library/logging.html) - Logging facility for Python
* [verboselogs](https://pypi.org/project/verboselogs/) - Verbose logging level for Python's logging module

### Future Features

  - Manage maximum number of calls throught access tokens 
  - Classify multiple images at once 
  - Possibility to switch from classification to object detection and back
  - Display detected object boundaries 

### Authors

* **[Enrico Da Rodda](https://github.com/enricodarodda)** - *Hackerman* 
* **[Fabio De Benetti](https://github.com/FabioDeBenetti)** - *BennyD* 
* **[Federico Fogolin](https://github.com/FedericoFogolin)** - *SwagyFog* 
* **[Lorenzo Pinto](https://github.com/LorenzoPinto04)** - *MisterP* 

### License
----

MIT


**Free Software, Hell Yeah!**
