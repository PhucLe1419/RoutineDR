from DatabaseConfiguration.database_mysql import connect_mysql
# from routine_project.Common.connect import connect_database
from rest_framework import status
from rest_framework.response import Response

special_char = "!@#$%^&*()-+?_=,<>/"

mdb = connect_mysql()
cursor = mdb.cursor()


def insert_data_user(data1, data2, data3, data4, data5, data6):
    list_data = [data1, data2, data3, data4, data5, data6]
    data_ins = "insert into login_user (user, password, ho, ten, email, sdt) values (%s, %s, %s, %s, %s, %s) "
    cursor.execute(data_ins, list_data)
    mdb.commit()


