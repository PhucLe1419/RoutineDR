from DatabaseConfiguration.database_mysql import  connect_mysql
from routine_project.Common.decorator import handle_api_swagger
# from routine_project.Common.connect import connect_database
from routine_project.Common.utils import handle_error, handle_success, CommonError
from rest_framework import status

special_char = "!@#$%^&*()-+?_=,<>/"

mdb = connect_mysql()
cursor = mdb.cursor()
def insert_data_user(data1, data2,data3,data4,data5,data6):
    try:
        list_data = [data1, data2, data3, data4, data5, data6]
        data_ins = "insert into login_user (user, password, ho, ten, email, sdt) values (%s, %s, %s, %s, %s, %s) "
        cursor.execute(data_ins, list_data)
        mdb.commit()
        return handle_success([])
    except Exception as e:
        print(e)
        return handle_error(e, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)