import mysql.connector
from mysql.connector import Error

def connect_mysql():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="routine_shop"
        )
        print("connect database success!!")
        return mydb
    except Error as e:
        return "Connect database fail!!".format(e)

connect_mysql()