from django.db import models
from marshmallow import fields
from marshmallow import Schema


class create_new_user(Schema):
    user = fields.Str(required=True)
    password = fields.Str(required=True)
    ho = fields.Str(required=True)
    ten = fields.Str(required=True)
    email = fields.Str(required=True)
    sdt = fields.Int(required=True)

class login_user(Schema):
    user = fields.Str(required=True)
    password = fields.Str(required=True)

# Create your models here.
