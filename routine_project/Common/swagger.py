import collections
from typing import Dict

from drf_yasg import openapi
from marshmallow import fields
from rsa import decrypt


def create_swagger_params(list_params, params_in=openapi.IN_QUERY):
    """Create swagger query string from list of parameters

    Args:
        list_params (list): list of parameters
            ex: [('page','number'), ('record_id','string'), ...]

    Returns:
        list openapi parameter
    """
    return [
        openapi.Parameter(
            item[0],
            in_=params_in,
            type=item[1],
            description=item[2] if len(item) >= 3 else None,
            enum=item[3] if len(item) >= 4 else None,
            format=item[4] if len(item) >= 5 else None,
            default=item[5] if len(item) >= 6 else None,
        )
        for item in list_params
    ]


def convert_to_swagger_field_type(field_schema):
    field_type = openapi.TYPE_STRING
    if isinstance(field_schema, fields.Raw):
        field_type = openapi.TYPE_FILE
    if isinstance(field_schema, fields.Nested):
        field_type = openapi.TYPE_OBJECT
    elif isinstance(field_schema, fields.Dict):
        field_type = openapi.TYPE_OBJECT
    elif isinstance(field_schema, fields.Boolean):
        field_type = openapi.TYPE_BOOLEAN
    elif isinstance(field_schema, fields.Number):
        field_type = openapi.TYPE_NUMBER
    elif isinstance(field_schema, fields.List):
        field_type = openapi.TYPE_ARRAY
    return field_type


def marshmallow_generate_manual_params(schema):
    list_params = []
    for key, field_schema in schema.fields.items():
        openapi_type = convert_to_swagger_field_type(field_schema)
        enum = None
        format = None
        description = field_schema.metadata.get("description", None)
        if field_schema.validate and field_schema.validate.choices:
            choices = field_schema.validate.choices
            enum = choices
        list_params.append((key, openapi_type, description, enum, format))

    return list_params


def marshmallow_to_swagger(field_name: str, field_schema: fields.Field):
    """
    Convert marshmallow to openapi schema

    :param field_name: field's name
    :param field_schema: marshmallow type
    :return: openapi doc
    """
    # if field_name == "file_hihi":
    #     print(field_name)
    field_type = type(field_schema)
    openapi_type = openapi.TYPE_STRING
    kwargs = {}
    if isinstance(field_schema, fields.Raw):
        kwargs["format"] = openapi.FORMAT_BINARY

    if field_schema.validate and hasattr(field_schema.validate, "choices"):
        choices = field_schema.validate.choices
        kwargs["enum"] = choices
    if isinstance(field_schema, fields.Nested):
        return open_api_schemas(field_schema.schema)
    elif isinstance(field_schema, fields.Dict):
        openapi_type = openapi.TYPE_OBJECT
    elif isinstance(field_schema, fields.Boolean):
        openapi_type = openapi.TYPE_BOOLEAN
    elif isinstance(field_schema, fields.Number):
        openapi_type = openapi.TYPE_NUMBER
    elif isinstance(field_schema, fields.List):
        item_type = openapi.TYPE_STRING
        if isinstance(field_schema.inner, fields.Dict):
            item_type = openapi.TYPE_OBJECT
        if isinstance(field_schema.inner, fields.Nested):
            properties, required_fields = open_api_schemas(
                field_schema.inner.schema, get_properties=True
            )
            return openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(
                    type=openapi.TYPE_OBJECT,
                    properties=properties,
                    required=required_fields,
                ),
            )

        swagger_type = openapi.Schema(
            type=openapi.TYPE_ARRAY,
            # description="Object",
            items=openapi.Items(type=item_type, **kwargs),
        )
        return swagger_type
    return openapi.Schema(type=openapi_type, **kwargs)


def open_api_schemas(schema, get_properties=False, swagger_schema=None):
    required_fields = []
    if not schema and not swagger_schema:
        return None
    if swagger_schema:
        for key, val in swagger_schema.items():
            if val["required"]:
                required_fields.append(key)
            swagger_schema[key] = collections.OrderedDict(val["prop"])
    else:
        swagger_schema = {}

    if schema:
        for field_name in schema.fields:
            field_schema = schema.fields[field_name]
            if field_schema.data_key:
                field_name = field_schema.data_key
            swagger_schema[field_name] = marshmallow_to_swagger(
                field_name, field_schema
            )
            if field_schema.required is True:
                required_fields.append(field_schema.name)
    if get_properties:
        return swagger_schema, required_fields
    swagger_schema_ordered = {
        k: swagger_schema[k] for k in required_fields if swagger_schema.get(k)
    }
    swagger_schema_ordered.update(
        {k: v for k, v in swagger_schema.items() if k not in required_fields}
    )
    request_body = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=required_fields,
        properties=swagger_schema_ordered,
    )
    return request_body
