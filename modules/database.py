import sqlite3
from modules import mylogger as ml

class RootDatabase():
    def __init__(self,dbname=None",max_tables=10000):
        self.dbname = dbname
        self.conn = None
        self.c = None
        self.l = ml.Logger()

    def __connect(self,db):
        if self.conn is None:
            self.conn = sqlite3.connect(f'{db}.db')
            self.c = self.conn.cursor()

    def __disconnect(self):
        self.conn.close()
    
    def __list_tables(self):
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables=(self.c.fetchall())
        return tables

    def __create_table_parser(self,mydict):
        self._check_dict(mydict)
        sql_params = ""
        i = 0
        for col in mydict:
            if not isinstance(mydict[col],tuple):
                raise TypeError(f"Invalid type for sql_parameters {type(mydict[col])} --> it must be a tuple")
            sql_line = f"{col} "
            for param in mydict[col]:
                sql_line += param+" "
            if i!=len(mydict.keys())-1:
                sql_line += ","
            sql_params += sql_line
            i+=1
        return sql_params
    
    def create_table(self,name,columns):
        params = self.__create_table_parser(columns)        
        command = f'''CREATE TABLE IF NOT EXISTS {name} ({params})'''
        self.c.execute(command)
        self.conn.commit()
        self.l.info(f"SQL: Created table with name {name} and {len(columns)} columns")
    


class Database(RootDatabase):
    def __init__(self,dbname="results",max_tables=10000):
        super().__init__(dbname,max_tables)

    def create_datacapture(self):
        def create_simulation(self):
            cols = {
            "Country" : ("VARCHAR(255)","NOT NULL"),
            "Total cases" : ("INT"),
            "New Cases" : ("INT"),
            "Total Deaths" : ("INT"),
            "New deaths" : ("INT"),
            "Total Recovered" : ("INT"),
            "Active Cases" : ("INT"),
            "Serious" : ("INT"),
            "Total Cases/1M pop" : ("INT"),
            "Deaths/1M pop" : ("INT"),
            "Total tests" : ("INT"),
            "Tests/1M pop" : ("INT"),
            "Population" : ("INT"),
        }
