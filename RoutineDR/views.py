from django.shortcuts import render
from routine_project.Common.decorator import handle_api_swagger
# from routine_project.Common.connect import connect_database
from routine_project.Common.utils import handle_error, handle_success, CommonError
from rest_framework import status
# from RoutineDR.query_market import test_query
from RoutineDR.models import create_new_user
from RoutineDR.models import login_user
from DatabaseConfiguration.database_mysql import connect_mysql
from DatabaseConfiguration.query_data import special_char
from DatabaseConfiguration.query_data import insert_data_user


# Create your views here.
db = connect_mysql()
cursor = db.cursor()
@handle_api_swagger(create_new_user(),"POST")
def create_user(request):
    try:
        request_body = login_user().load(request.data)
        user_name = request_body.get("user")
        pass_w = request_body.get("password")
        ho_user = request_body.get("ho")
        ten_user = request_body.get("ten")
        email = request_body.get("email")
        sdt = request_body.get("sdt")
        if user_name is None or pass_w is None:
            raise CommonError("Error user name or password is None")
        if ho_user is None or ten_user is None:
            raise CommonError("Error ho and ten is None")
        if email is None or sdt is None:
            raise CommonError("Error email or sdt is None ")
        # check data
        cursor.execute(f"select user from login_user where user = '{user_name}'")
        check_user = cursor.fetchall()
        if check_user:
            return handle_error("This user is already in the system. Please choose another username ")
        if not any(char in special_char for char in pass_w):
            return handle_error([], "Password not have special character!")
        data_insert = insert_data_user(user_name, pass_w, ho_user, ten_user, email, sdt)
        return data_insert
    except Exception as e:
        print(e)
        return handle_error(e, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@handle_api_swagger(login_user(),"POST")
def login(request):
    try:
        request_body = login_user().load(request.data)
        user_name = request_body.get("user")
        pass_w = request_body.get("password")
        if user_name is None or pass_w is None:
            raise CommonError("User or password is None")
        # check user
        cursor.execute(f"select user, password from login_user where user = '{user_name}'")
        check_user = cursor.fetchall()
        if not check_user:
            return handle_error("This user is wrong. Please check user again!!")
        for check_pass in check_user:
            if pass_w != check_pass[1]:
                return handle_error("password is wrong")
            else:
                return handle_success([])
    except Exception as e:
        print(e)
        return handle_error(e, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



