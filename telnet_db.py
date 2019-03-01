import time
import os

from telnetlib import Telnet
import pyodbc

db_file = os.path.realpath(__file__)
CONN_STRING = r'DRIVER=Driver do Microsoft Access (*.mdb);DBQ=c:\users\marwan abdelatti\desktop\py_telnet_db-master\test_1.mdb'

def fetch_data():
        with Telnet('localhost', 9055, 10) as tn:
                print('Successfully connected to port.')
                res = tn.read_until(b'AAAAAAAAAAAAAAAAAAAAAAAA', 5).splitlines()

        record = [record[:record.index(b'\t')].decode('utf-8') for record in res[1:]]
        return record

def connect_to_db(CONN_STRING):
        conn = pyodbc.connect(CONN_STRING)
        cursor = conn.cursor()
        print('Successfully connected to database.')
        return(cursor)

def clear_db(cursor):
        # Clear ALL raw data before adding the new records        
        cursor.execute('DELETE FROM raw_data')
        cursor.commit()

def push_data(record_list, cursor):

        for record in record_list:
                cursor.execute('''INSERT INTO raw_data (Tag_ID)
                                VALUES('%s')''' %record)
        cursor.commit()

if __name__ == "__main__":
        cursor = connect_to_db(CONN_STRING)
        while cursor:
                clear_db(cursor)
                push_data(fetch_data(), cursor)
                time.sleep(10)