from database_mysql import connect_mysql
from query_mysql import table_login_user
import mysql.connector
from mysql.connector import Error

db = connect_mysql()
def create_table(data):
    try:
        db.cursor().execute(data)
    except Error as e:
        print("create table error!".format(e))




