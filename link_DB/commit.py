# -*- coding: utf-8 -*-
from . import psql
import pandas.io.sql as sqlio
import time

class COMMIT:
    def __init__(self):
        self.commit = []
    
    def link(self, use_DB: str, DB: str):
        if use_DB == 'PSQL':
            Psql = psql.PSQL(DB)
            self.commit = Psql.link()
            
    def close(self):
        self.commit.close()
        
        
    def query_base(self, schema: str, table: str, column: str):
        data = sqlio.read_sql_query(f'''
                                    select {column}
                                    from {schema}.{table}
                                    ''',self.commit)
        return data
        
       