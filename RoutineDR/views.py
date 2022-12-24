from django.shortcuts import render

# from routine_project.Common.connect import connect_database

from rest_framework import status
# from RoutineDR.query_market import test_query
from RoutineDR.models import create_new_user
from RoutineDR.models import login_user
from DatabaseConfiguration.database_mysql import connect_mysql
from DatabaseConfiguration.query_data import special_char
from DatabaseConfiguration.query_data import insert_data_user
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
db = connect_mysql()
cursor = db.cursor()


@api_view(["POST"])
def create_user(request):
    try:
        request_body = create_new_user().load(request.data)
        user_name = request_body.get("user")
        pass_w = request_body.get("password")
        ho_user = request_body.get("ho")
        ten_user = request_body.get("ten")
        email = request_body.get("email")
        sdt = request_body.get("sdt")

        # check data
        cursor.execute(f"select user from login_user where user = '{user_name}'")
        check_user = cursor.fetchall()
        if check_user:
            return Response({"message": "This user is already in the system. Please choose another username "})
        if not any(char in special_char for char in pass_w):
            return Response({"message": "Password not have special character!"})
        data_insert = insert_data_user(user_name, pass_w, ho_user, ten_user, email, sdt)
        return data_insert
    except Exception as e:
        print(e)
        return Response(e)


@api_view(["POST"])
def login(request):
    try:
        request_body = login_user().load(request.data)
        user_name = request_body.get("user")
        pass_w = request_body.get("password")
        # check user
        cursor.execute(f"select user, password from login_user where user = '{user_name}'")
        check_user = cursor.fetchall()
        if not check_user:
            return Response(content_type="This user is wrong. Please check user again!!")
        for check_pass in check_user:
            if pass_w != check_pass[1]:
                return Response(content_type="password is wrong")
            else:
                return Response(content_type="Login user success!")
    except Exception as e:
        print(e)
        return Response(data=e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
