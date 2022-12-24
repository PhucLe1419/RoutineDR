import mysql.connector
from mysql.connector import Error
from rest_framework.response import Response


def connect_mysql():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="routine_shop"
        )
        return mydb
    except Exception as e:
        return Response(e)

