#! /usr/bin/ven python
from marshmallow import Schema, fields, post_load,validates


class UserSchema(Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True)

    @validates('name')
    def name_validate(self, value):
        pass

    @post_load
    def age_incre(self, data):
        if 'age' in data and data['age'] > 0:
            age = data['age'] + 5
        return data


class UserDumpSchema(Schema):
    name = fields.String()
