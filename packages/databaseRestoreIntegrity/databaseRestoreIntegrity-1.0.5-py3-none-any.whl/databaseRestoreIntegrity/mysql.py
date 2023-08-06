#!/usr/bin/env python3

import mysql.connector
import re
import csv
import os

class mysqlReadData:

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def connection(self):
        try:
            mydb = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password
        )
        except:
            print(f'Connection is not successful')
        return mydb

    def _db_list(self):
        dbs = []
        sql_query = "show databases"
        try:
            conn = self.connection()
            mycursor = conn.cursor()
            mycursor.execute(sql_query)
            # mycursor.execute('show databases')
            for x in mycursor:
                dbs.append(*x)
        except:
            print(f'database list not succedd')
        return dbs

    def _table_list(self):
        tables_names = []
        conn = self.connection()
        dbs = self._db_list()
        for x in dbs:
            sql_query = "USE " + x
            tables = conn.cursor()
            tables.execute(sql_query)
            tables.execute("show tables")
            for t in tables:
                tables_names.append("{}.{}".format(x, *t))   
        return tables_names

    def _records_count(self):
        records_count = []
        conn = self.connection()
        t_name = self._table_list()
        for c in t_name:
            sql_query = "select count(*) from " + c
            r = conn.cursor()
            r.execute(sql_query)
            for count in r:
                records_count.append("{},{}".format(c, *count))  
        return records_count   

    def _create_tmp_file(self, name):
        self.name = name
        records = self._records_count()
        f = open(self.name, 'w+')
        for data in records:
            sql_query = ("{}{}{}{}".format('INSERT INTO ', self.name, ' (tables_name, records_count, hostname) VALUES ', (data.split(",")[0], data.split(",")[1], self.host)))
            f.write("{}\n".format(sql_query))
        f.close()
        
    def _insert_data(self, name):
        conn = self.connection()
        self.name = name
        ct = conn.cursor()
        table_drop_query = ("{}{}".format('DROP TABLE IF EXISTS ', self.name))
        ct.execute("CREATE DATABASE IF NOT EXISTS CheckDBsTableConsistency")
        ct.execute("USE CheckDBsTableConsistency")
        ct.execute(table_drop_query)
        ct.execute("{}{}{}".format('CREATE TABLE IF NOT EXISTS ', self.name, ' (tables_name VARCHAR(255), records_count VARCHAR(255), hostname VARCHAR(244))'))
        f = open(self.name, 'r')
        lines = f.readlines()
        count = 0
        for line in lines:
            count += 1
            sql_query = ("{}".format(line.strip()))
            ct.execute(sql_query)
            conn.commit()
        f.close()
        os.remove(self.name)
        conn.close()
