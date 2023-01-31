# coding=utf-8
"""
utils.py

@Author:    Emotu Balogun
@Date:      January 02, 2019
@Time:      3:42 PM

This module contains a number of utility functions useful throughout our application.
No references are made to specific models or resources. As a result, they are useful with or
without the application context.
"""
from datetime import date, datetime
from math import ceil

from bson.objectid import ObjectId
import json
from marshmallow import ValidationError, EXCLUDE
from pymodm import MongoModel, EmbeddedMongoModel
from pymodm.queryset import QuerySet


class CustomJSONEncoder(json.JSONEncoder):
    """ JSON encoder that supports date formats """

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return datetime.combine(date, datetime.min.time()).isoformat()

        # Implement json decoder for ObjectId if needed
        if isinstance(obj, ObjectId):
            return str(obj)

        if isinstance(obj, bytes):
            return str(obj.decode("utf-8"))

        if isinstance(obj, (MongoModel, EmbeddedMongoModel)):
            return obj.to_son().to_dict()

        return json.JSONEncoder.default(self, obj)


def marshal(resp, schema):
    """
    prepares the response object with the specified schema
    :param resp: the falcon response object
    :param res: the object
    :param schema: the schema class that should be used to validate the response
    :return: falcon.Response
    """
    data = resp
    resp_ = None

    if isinstance(data, list) or isinstance(data, QuerySet):
        r = list(data)
        resp_ = schema().dump(r, many=True)
    if isinstance(data, dict):
        try:
            resp_ = schema().load(data=data, unknown=EXCLUDE)
        except ValidationError as e:
            print("Errors", e)
            raise ValidationFailed(data=e.messages)
    return resp_


def convert_dict(data, indent=None, to_json=False):
    json_str = json.dumps(data, indent=indent, cls=CustomJSONEncoder)
    if to_json:
        # json_str = json_str.rstrip("'").lstrip("'")
        json_str = json.loads(json_str)
    return json_str


def clean_kwargs(ignored_keys, data):
    """
    Removes the ignored_keys from the data sent

    ignored_keys: keys to remove from the data (list or tuple)
    data: data to be cleaned (dict)

    returns: cleaned data
    """

    for key in ignored_keys:
        data.pop(key, None)

    return data


def roundUp(n, d=2):
    d = int('1' + ('0' * d))
    return ceil(n * d) / d


def populate_obj(obj, data):
    """
    Populates an object with the data passed to it

    param obj: Object to be populated
    param data: The data to populate it with (dict)

    returns: obj populated with data


    """
    for name, value in data.items():
        if hasattr(obj, name):
            # print(name, value)
            if isinstance(value, float):
                value = roundUp(value)
            setattr(obj, name, value)

    return obj
