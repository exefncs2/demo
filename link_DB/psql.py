# -*- coding: utf-8 -*-
import psycopg2
import configparser

class PSQL:
    def __init__(self, DB):
        self.DB = DB
        self.info_dict = configparser.ConfigParser()
        self.info_dict.read('./source/demo_login_info.ini')
        
    def link(self):
        info_dict = self.info_dict['login']
        connect = psycopg2.connect(
                                   database=self.DB,
                                   host=info_dict['ip'],
                                   port=info_dict['port'],
                                   user=info_dict['user'],
                                   password=info_dict['password'],
                                   )
        return connect