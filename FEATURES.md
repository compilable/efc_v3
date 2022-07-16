Features to be implemented will be documented in this file.
Versioning based on [Semantic Versioning 2.0.0](http://semver.org/) format.

``` Create a separate branch for each feature/fix and create a pull request merge with the master branch.```

# version 1.0.0
- Capture input parms for below operations:
```
Encrypt:
    1. source location [files to encrypt]
    2. destination location
    3. operation - e
    4. index file password
    5. data encryption password file location 
    # INIT :  check for existing db in destination or create new DB
```
    
```
Decrypt:
    1. source location [files to decrypt]
    2. destination location
    3. operation - d
    4. index file password
    5. data encryption password file location 
    # INIT :  check for existing db in source
```
- USE CASE 1 : running for the 1st time : new env

```
### Encrypt 
1. list all files to be encrypted in the source folder
2. insert the file details into table
3. read the files from table
4. encrypt the files to desination
5. update the table for encrypted file hash

### Decrypt 
1. list all files from table which are encrypted.
2. decrypt the files to a given location (folder structure based on the fq_path)
3. verify the original file hash with restored file hash
```

- USE CASE 2 : existing env
```
1. read the DB to obtain the existing file list
2. read the FS to obtain the file list
3. insert the file not in the DB to table
4. check the existing files based on the name/hash [found -> ignore, new -> insert to DB ]
5. read the files from table
6. encrypt the files to desination
7. update the table for encrypted file hash
```
