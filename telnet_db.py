import time
from telnetlib import Telnet
import pyodbc

CONN_STRING = r'DRIVER=Driver do Microsoft Access (*.mdb);DBQ=C:\Users\Marwan Abdelatti\Desktop\test_1.accdb.mdb'

def fetch_data():
        with Telnet('localhost', 9055, 10) as tn:
                res = tn.read_until(b'AAAAAAAAAAAAAAAAAAAAAAAA', 5).splitlines()

        record = [record[:record.index(b'\t')].decode('utf-8') for record in res[1:]]
        return record

def connect_to_db(CONN_STRING):
        conn = pyodbc.connect(CONN_STRING)
        cursor = conn.cursor()
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
        while True:
                clear_db(connect_to_db(CONN_STRING))
                push_data(fetch_data(), connect_to_db(CONN_STRING))
                time.sleep(10)