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
```

### Now create and run a python scrip using the content below
```
from databaseRestoreIntegrity import mysql
from tabulate import tabulate
import os

src_db_host = os.environ['SRC_DB_HOST']
src_db_pass = os.environ['SRC_DB_PASS']
src_db_user = os.environ['SRC_DB_USER']

dst_db_host = os.environ['DST_DB_HOST']
dst_db_pass = os.environ['DST_DB_PASS']
dst_db_user = os.environ['DST_DB_USER']


database = mysql.mysqlRestroeCheck(src_db_host, src_db_user, src_db_pass)
database1 = mysql.mysqlRestroeCheck(dst_db_host, dst_db_user, dst_db_pass)
database._create_tmp_table('restore_rds')
database1._create_tmp_table('actual_rds')

def check_consistency():
    unconsistent_tabels = []
    conn = database.connection()
    check_consistency = conn.cursor()
    check_consistency.execute("USE restore_consistency")
    check_consistency.execute("SELECT tables_name,records_count,hostname FROM (SELECT tables_name,records_count,hostname FROM restore_rds UNION ALL SELECT tables_name,records_count,hostname FROM actual_rds) tbl GROUP BY tables_name, hostname, records_count HAVING count(*) = 1 ORDER BY tables_name")

    result = check_consistency.fetchall()
    print(tabulate(result, headers=['tables_name', 'records_count'], tablefmt='psql'))
check_consistency()
```




