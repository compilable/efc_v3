# Encrypt Folder Content v3.
## _symmetrically encrypt files and folders by keeping track of each file pre and post-meta-data during the encryption process._

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Simple python script to use GPG symmetric encryption to protect data.

## Features:
- PnP (Use the python and built-in GPG tools)
- Two layers of encryption.
- Cloud-ready. (Can be used to encrypt content before uploading to open cloud providers.)
- Can be automated. 

## Requirements and Dependencies:

Requires [Python](https://www.python.org/) 3.8.10+ to run.

| Requirement | Download | Version |
| ------ | ------ | ------ |
| Python | https://www.python.org/ | 3.8.10+ |
| pip | https://pip.pypa.io/en/stable/installation/ | 20.0.2+ |
| GPG | https://gnupg.org/download/ | 2.2.19 |
| TAR | https://www.gnu.org/software/tar/ | 1.30 |

## Installation:

Install the efc package using pip package manager.

```sh
cd efc_v3
pip install efc_v3
evc_v3 <PARAMS>
```

## Usage:

Use the below commands as the parameters:

| Commands | Description | Optional | Default |
| ------ | ------ | ------ |------ |
| -o | operation (e for encrypt, d for decrypt) | No | e |
| -s | source folder location | No | N/A |
| -d | destination folder location | No | N/A |
| -index-password | password to encrypt the `index file`. | Yes | N/A |
| -password | password to encrypt the `file content`.  | No | N/A |
| -i | index file name and location | Yes | an index file will be created with `.db` on the source location. |
| -r | restore folder location | Yes | N/A |
| -allow-duplicate | allow duplicate files during encryption process | Yes | False |
| -random-file-names | generate random names for files | Yes | False |
| -ignore-types | list of file types (extensions) to ignore. | Yes | N/A |

## Running Tests:
Use the sample files inside the `test` folder with the below commands:

### _encrypt:_
Below command should `encrypt` the all the content found inside the `test/test_data/source_location` to the folder : `test/test_data/destination_location`.
```
evc_v3 -o e -s test/test_data/source_location -d test/test_data/destination_location
```

### _decrypt:_
Below command should `decrypt` the all the content found inside the `test/test_data/destination_location` to the folder : `test/test_data/source_location`.
```
evc_v3 -o d -s test/test_data/destination_location  -d test/test_data/source_location
```

## Reference:
- [gnupg - official website](https://www.gnupg.org/download/ "gnupg - official")

## License:
- MIT license (MIT)


