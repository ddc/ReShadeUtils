#! /usr/bin/env python3
#|*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# * Python            : 3.6
#|*****************************************************
# # -*- coding: utf-8 -*-

import psycopg2
from src.utils import utils
################################################################################
################################################################################
################################################################################ 
class PostgreSQL():
    def __init__(self, log):
        database = utils.get_database()
        self.log = log
        self.pg_host             = database.host
        self.pg_port             = database.port
        self.pg_dbname           = database.db_name
        self.pg_username         = database.username
        self.pg_password         = database.password
################################################################################
################################################################################
################################################################################ 
    def create_connection(self):
        try:
            conn = psycopg2.connect(dbname=self.pg_dbname,
                                    user=self.pg_username,
                                    password=self.pg_password,
                                    host=self.pg_host,
                                    port=self.pg_port)
        except psycopg2.Error as e:
            conn = None
            msg = f"PostgreSQL:Cannot Create Database Connection ({self.pg_host}:{self.pg_port})"
            self.log.error(f"{msg}\n({e})")
            self.log.exception("PostgreSQL",exc_info=e)
            print(f"{msg}\n({e})")
            #utils.wait_return()
            raise psycopg2.Error(e)
        finally:
            return conn
################################################################################
################################################################################
################################################################################
    def execute(self, sql:str):
        #result = None
        conn = self.create_connection()
        if conn is not None:
            try:
                if sql is not None and len(sql) > 0:
                    cur = conn.cursor()
                    cur.execute(sql)
                    cur.close()
                    conn.commit()
            except (Exception, psycopg2.DatabaseError) as e:
                #result = e
                self.log.exception("PostgreSQL",exc_info=e)
                self.log.error(f"Sql:({sql})")
                print(str(e))
                #utils.wait_return()
                raise psycopg2.DatabaseError(e)
            finally:
                if conn is not None:
                    conn.close()
                #return result
################################################################################
################################################################################
################################################################################
    def select(self, sql:str):
        conn = self.create_connection()
        if conn is not None:
            try:
                if sql is not None and len(sql) > 0:
                    finalData = {}
                    cur = conn.cursor()
                    cur.execute(sql)
                    rows = cur.fetchall()
                    colnames = [desc[0] for desc in cur.description]
                    cur.close()
                    for lineNumber, data in enumerate(rows):
                        finalData[lineNumber] = {}
                        for columnNumber, value in enumerate(data):
                            finalData[lineNumber][colnames[columnNumber]] = value
            except (Exception, psycopg2.DatabaseError) as e:
                self.log.exception("PostgreSQL",exc_info=e)
                self.log.error(f"Sql:({sql})")
                print(str(e))
                #utils.wait_return()
                #raise psycopg2.DatabaseError(e)
            finally:
                if conn is not None:
                    conn.close()
                return finalData
################################################################################
################################################################################
################################################################################
