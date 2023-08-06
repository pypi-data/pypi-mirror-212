# MySQL restore integrity check
Module can be used to test the database integrigity after restore the database. It will compare tables and show the only that tables in tabular format, Which had diffrencial records in after restore. 

## Requirements
- python3.6 or above
- tablular and os python plugin should be installed using pip3

## How to use
```
$ pip3 install databaseRestoreIntegrity
$ export SRC_DB_HOST='origin_database_hostname'
$ export SRC_DB_USER='origin_database_username'
$ export SRC_DB_PASS='origin_database_password'
$ export DST_DB_HOST='restored_database_hostname'
$ export DST_DB_USER='restored_database_username'
$ export DST_DB_PASS='restored_database_password'