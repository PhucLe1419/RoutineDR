from django.http import HttpResponse, JsonResponse
from rest_framework import status
from marshmallow import ValidationError
import requests
from django.core.cache import cache

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


def render_schema_view(ui="swagger"):
    # user_email = config.get("USER_DEBUG")
    # if user_email:
    #     try:
    #         db_root = getattr(connect.client, "Tenants")
    #         user_info = db_root[constants.TB_USER].find_one({"email": user_email})
    #         tenant_id = user_info.get("tenants")
    #         user_tenant_info = check_user_crm(tenant_id, user_email)
    #         token = encode_token(user_tenant_info, tenant_id)
    #         cache.set("swagger_default_token", token)
    #     except Exception:
    #         pass
    schema_view = get_schema_view(
        openapi.Info(
            title="TRADING-BOT API",
            default_version="v1",
            description="API",
            # terms_of_service="https://www.google.com/policies/terms/",
            # contact=openapi.Contact(email="phamvanthieu1798@gmail.com"),
            # license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
    )
    if ui == "swagger":
        return schema_view.with_ui("swagger", cache_timeout=0)

    if ui == "redoc":
        return schema_view.with_ui("redoc", cache_timeout=0)

    return schema_view.without_ui(cache_timeout=0)


def handle_error(error, message="UNKNOWN ERROR", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
    if isinstance(error, CommonError):
        message = error.message or message
        status_code = error.status_code or status_code
        return JsonResponse({"error": str(message), "status_code": status_code}, status=status_code,
                            json_dumps_params={'ensure_ascii': False})

    if isinstance(error, ValidationError):
        error = error.normalized_messages()
        error_message = format_marshmallow_error(error)
        return JsonResponse({"error": error_message, "status_code": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST, json_dumps_params={'ensure_ascii': False})
    return JsonResponse({"error": str(error), "status_code": status_code}, status=status_code,
                        json_dumps_params={'ensure_ascii': False})


def handle_success(data, status_code=status.HTTP_200_OK, message="success", code=0, item_ex=[], ex_mess="", ex_err_mess=""):
    if isinstance(data, JsonResponse):
        return data

    if isinstance(data, HttpResponse):
        return data

    if isinstance(data, requests.models.Response):
        response = HttpResponse(
            content=data.content,
            status=data.status_code,
            content_type=data.headers['Content-Type']
        )
        return response

    return JsonResponse({"item": data, "message": message, "status_code": status_code, "code": code, "ItemExcelError": item_ex,
                         "ExMessage": ex_mess, "ExcelErrorMessage": ex_err_mess}, status=status_code,json_dumps_params={'ensure_ascii': False})


def handle_warning(message, data="", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
    if isinstance(message, JsonResponse):
        return message

    if isinstance(message, HttpResponse):
        return message

    if isinstance(message, requests.models.Response):
        response = HttpResponse(
            content=message.content,
            status=message.status_code,
            content_type=message.headers['Content-Type']
        )
        return response
    return JsonResponse({"error": message, "data": data, "status_code": status_code}, status=status_code,
                        json_dumps_params={'ensure_ascii': False})


def format_marshmallow_error(error):
    """Return marshmallow error message with structure: {"<field_id>": "<error_message>"}"""
    message = ""
    for key, value in error.items():
        message += f"`{key} : {value}`. "

    return message


class Error(Exception):
    pass


class CommonError(Error):
    def __init__(self, message='INTERNAL SERVER ERROR', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super(CommonError, self).__init__(message)














