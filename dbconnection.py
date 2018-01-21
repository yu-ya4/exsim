import MySQLdb
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def get_db_connection():
    '''
    Get database connection
    '''
    db = os.environ.get('DB')
    try:
        if db == 'local':
            return MySQLdb.connect(host=os.environ.get('LOCAL_DB_HOST'), user=os.environ.get('LOCAL_DB_USER'), passwd=os.environ.get('LOCAL_DB_PASSWD'), db=os.environ.get('LOCAL_DB_DATABASE'), charset=os.environ.get('CHARSET'))
        elif db == 'ieyasu':
            return MySQLdb.connect(host=os.environ.get('IEYASU_DB_HOST'), user=os.environ.get('IEYASU_DB_USER'), passwd=os.environ.get('IEYASU_DB_PASSWD'), db=os.environ.get('IEYASU_DB_DATABASE'), charset=os.environ.get('CHARSET'), port=int(os.environ.get('IEYASU_DB_PORT')))
        elif db == 'ieyasu-berry':
            return MySQLdb.connect(host=os.environ.get('IEYASU_DB_HOST'), user=os.environ.get('IEYASU_DB_USER'), passwd=os.environ.get('IEYASU_DB_PASSWD'), db=os.environ.get('IEYASU_DB_DATABASE'), charset=os.environ.get('CHARSET'), port=int(os.environ.get('IEYASU_BERRY_DB_PORT')))
        elif db == 'ieyasu-local':
            return MySQLdb.connect(host=os.environ.get('IEYASU_DB_HOST'), user=os.environ.get('IEYASU_DB_USER'), passwd=os.environ.get('IEYASU_DB_PASSWD'), db=os.environ.get('IEYASU_DB_DATABASE'), charset=os.environ.get('CHARSET'))
        else:
            print('Error: please select correct database')
            exit()
    except MySQLdb.Error as e:
        print('MySQLdb.Error: ', e)
        exit()
