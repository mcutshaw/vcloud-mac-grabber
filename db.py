#!/usr/bin/python3
import hashlib
import configparser
import sqlite3

class ialab_db:

    def __init__(self,config):
        try:
            self.db = config['Database']['Database']
        except Exception as e:
            print("Config Error!")
            print(e)
            exit()
        try:    
            self.connect()
        except:
            print("Database Error!")
        tables = self.execute("SELECT name FROM sqlite_master WHERE type='table';")
        if ('macs',)  not in tables: 
            self.execute('''CREATE TABLE macs
                            (vapp TEXT TEXT NOT NULL,
                            vm TEXT NOT NULL,
                            mac TEXT);''')


    def close(self):
        self.conn.close()

    def connect(self):
        self.conn = sqlite3.connect(self.db)
        self.cur = self.conn.cursor()

    def execute(self,command):
        self.connect()
        self.cur.execute(command)
        self.conn.commit()
        text_return = self.cur.fetchall()
        self.close()
        return text_return

    def executevar(self,command,operands):
        self.connect()
        self.cur.execute(command,operands)
        self.conn.commit()
        text_return = self.cur.fetchall()
        self.close()
        return text_return

    def insertMAC(self, vapp, vm, mac):
        self.executevar('INSERT INTO macs VALUES(?,?,?)', (vapp, vm, mac))
