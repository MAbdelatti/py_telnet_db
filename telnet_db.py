import time
import os
import pathlib

from telnetlib import Telnet
import pyodbc

db_file = pathlib.Path(os.path.realpath(__file__)).parents[0]
db_file = db_file / 'EKanBan_Bin_Database_REV5.mdb'
print(db_file)
CONN_STRING = r'DRIVER=Driver do Microsoft Access (*.mdb);DBQ=%s'%db_file

def fetch_data():
        with Telnet('localhost', 9055, 10) as tn:
                print('Successfully connected to port.')
                res = tn.read_until(b'AAAAAAAAAAAAAAAAAAAAAAAA', 5).splitlines()

        record = [record[:record.index(b'\t')].decode('utf-8') for record in res[1:]]
        # returning (set) avoids duplicated records:
        return set(record)

def connect_to_db(CONN_STRING):
        conn = pyodbc.connect(CONN_STRING)
        cursor = conn.cursor()
        print('Successfully connected to database.')
        return(cursor)

def clear_db(cursor):
        # Clear ALL raw data before adding the new records        
        cursor.execute('DELETE FROM reader_data')
        cursor.commit()

def push_data(record_list, cursor):

        for record in record_list:
                cursor.execute('''INSERT INTO reader_data (EPC)
                                VALUES('%s')''' %record)
        cursor.commit()

if __name__ == "__main__":
        cursor = connect_to_db(CONN_STRING)
        while cursor:
                clear_db(cursor)
                push_data(fetch_data(), cursor)
                time.sleep(10)