from marshmallow import Schema, fields

"""
Marshmallow schemas stub code.

Automatic generation of marshmallow schemas from dataclasses

Marshmallow schemas can be used to:
1. Validate input data.
2. Deserialize input data to app-level objects.
3. Serialize app-level objects to primitive Python types.
   The serialized objects can then be rendered to standard formats such as JSON for use in an HTTP API.
"""


class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()


user_data = {
    "created_at": "2014-08-11T05:26:03.869245",
    "email": "ken@yahoo.com",
    "name": "Ken",
}
schema = UserSchema()
result = schema.load(user_data)

print(result)
