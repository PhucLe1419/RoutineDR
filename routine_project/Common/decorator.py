import json
import logging
import sys
import traceback
from datetime import datetime
from functools import wraps
from django.core.cache import cache
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.utils import unset
from rest_framework import status
from rest_framework.decorators import api_view
from tradingproject.Common.swagger import marshmallow_generate_manual_params, \
    create_swagger_params, open_api_schemas
API_RESPONSES = {
    "200": "Successfully.",
    "400": "Validation Error.",
    "500": "Server Error.",
}


class UploadSchema(SwaggerAutoSchema):
    def get_consumes(self):
        super(UploadSchema, self).get_consumes()
        return ["multipart/form-data"]


def generate_query_string(model_payload, model_query_string, form_data):
    try:
        query_string = []
        if model_query_string:
            query_string.extend(marshmallow_generate_manual_params(model_query_string))
            query_string = create_swagger_params(query_string)

        if form_data and model_payload:
            form_props = []
            form_props = marshmallow_generate_manual_params(model_payload)
            form_props = create_swagger_params(form_props, openapi.IN_FORM)
            query_string.extend(form_props)

        if cache.get("swagger_default_token"):
            token = cache.get("swagger_default_token")
            default_token = create_swagger_params(
                [("Authorization", "string", "Bearer Token", None, None, token)],
                openapi.IN_HEADER,
            )
            query_string.extend(default_token)

        if not query_string:
            return None
        return query_string
    except Exception:
        pass


def handle_api_swagger(
    model,
    method,
    # required_admin=False,
    # required_root=False,
    body_schema=None,
    model_query_string=None,
    form_data=False,
    # authenticate=True,
):
    query_string = generate_query_string(model, model_query_string, form_data)

    def outer(func):
        @swagger_auto_schema(
            method,
            request_body=open_api_schemas(
                model,
                swagger_schema=body_schema,
            )
            if not form_data
            else None,
            responses=API_RESPONSES,
            manual_parameters=query_string,
            auto_schema=UploadSchema if form_data else unset)
        @api_view([method])
        @wraps(func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner
    return outer