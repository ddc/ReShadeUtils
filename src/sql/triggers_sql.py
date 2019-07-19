#! /usr/bin/env python3
#|*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# * Python            : 3.6
#|*****************************************************
# # -*- coding: utf-8 -*-

from src.databases.databases import Databases
from src.utils import utils
################################################################################
################################################################################
################################################################################
class TriggersSql():
    def __init__(self, log):
        self.log = log
        self.database_in_use = utils.get_file_settings("Configs", "DatabaseInUse")
################################################################################
################################################################################
################################################################################        
    def create_triggers(self):
        if self.database_in_use == "sqlite":
            sql="""CREATE TRIGGER IF NOT EXISTS before_insert_configs
                    BEFORE INSERT ON configs
                    BEGIN
                        SELECT CASE
                            WHEN (SELECT count(*) FROM configs)IS 1 THEN
                            RAISE(ABORT, 'CANNOT INSERT INTO CONFIGS TABLE ANYMORE.')
                        END;
                    END;
            """
        elif self.database_in_use == "postgres":
            sql= """DROP TRIGGER IF EXISTS before_insert_configs ON configs;
                ------
                CREATE or REPLACE FUNCTION before_insert_configs_func()
                    returns trigger language plpgsql as $$
                    begin
                        RAISE unique_violation USING MESSAGE = 'CANNOT INSERT INTO CONFIGS TABLE ANYMORE';
                        return null;
                    end $$;        
                
                CREATE TRIGGER before_insert_configs
                    BEFORE INSERT ON configs 
                    for each row execute procedure before_insert_configs_func();
                ------
            ;"""
            
        databases = Databases(self.log)
        databases.execute(sql)
################################################################################
################################################################################
################################################################################
