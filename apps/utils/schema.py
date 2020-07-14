# -*-coding: utf-8 -*-

import datetime
from dateutil.relativedelta import relativedelta
from marshmallow import Schema, fields, post_load, validates, ValidationError


class QueryList(fields.Field):

    def __init__(self, element_type=str, **kwargs):
        self.element_type = element_type
        super(QueryList, self).__init__(**kwargs)

    def _deserialize(self, value, attr, data):
        result = super(QueryList, self)._deserialize(value, attr, data)
        errors = {}
        try:
            result = [self.element_type(i) for i in result.split(',')]
        except Exception as e:  # noqa
            errors[attr] = "Invalid value"

        if errors:
            raise ValidationError(errors, data=result)

        return result


class TimeSchema(Schema):
    start_time = fields.String()
    end_time = fields.String()
    interval_time = fields.Integer()

    @validates('start_time')
    def validates_start_time(self, value):
        try:
            datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError as e:  # noqa
            raise ValidationError('illegal start time')

    @validates('end_time')
    def validates_end_time(self, value):
        try:
            datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError as e:  # noqa
            raise ValidationError('illegal end time')

    # @validates_schema
    # def validates_schema(self, data):
    #     """
    #     schema 级别的验证，主要是针对各种数据之间依赖关系的验证
    #     """
    #     if 'interval_time' not in data:
    #         if data.get('start_time', '') == '':
    #             raise ValidationError('start_time is required')
    #         if data.get('end_time', '') == '':
    #             raise ValidationError('end_time is required')
    #         return True

    @post_load
    def process_delta(self, data):
        if 'interval_time' in data and data['interval_time'] > 0:
            end = datetime.datetime.now()
            start = end - relativedelta(days=data['interval_time'])

            data['start_time'] = start.strftime("%Y-%m-%d %H:%M:%S")
            data['end_time'] = end.strftime("%Y-%m-%d %H:%M:%S")
            data.pop('interval_time')

        return data


class PaginatorSchema(Schema):
    limit = fields.Integer(missing=10)
    page = fields.Integer(missing=1, validate=lambda p: p >= 1, required=True)

    @post_load
    def process_offset(self, data):
        data['offset'] = (data['page'] - 1) * data['limit']


class SortSchema(Schema):
    sort = fields.String()
    order = fields.String(missing='desc', validate=lambda o: o in ['desc', 'asc'])


class PaginatorTimeSchema(TimeSchema, PaginatorSchema):
    pass


if __name__ == '__main__':
    t, errors = PaginatorTimeSchema().load({})
    print t, errors
