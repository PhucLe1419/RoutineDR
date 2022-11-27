import mysql.connector

def connect_mysql():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="api_market"
        )

        return mydb
    except:
        return "Connect error!"
