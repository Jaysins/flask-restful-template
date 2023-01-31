"""
odm.py

@Author: Emotu Balogun
@Date: December 18, 2018

The base class for application services. All services that inherit from the parent class will carry basic functionality that can be
overridden. Functionality for each service class include:
    - create: Create a new object
    - create_many: Create multiple objects at once
    - update: Update an existing object
    - update_many: Update multiple objects at once
    - get: Retrieve an object by ID
    - get_by_ids: get an array of objects by a list of ids
    - query: Retrieve a collection of objects by query
    - delete: Delete an object by ID
    - delete_by_ids: Delete a collection of objects by query via ids

"""

from datetime import datetime
from ..base import utils
from bson.objectid import ObjectId


class ServiceFactory(object):
    """
    Service factory generator. This class will produce other service classes required by any application that uses it.
    """

    @classmethod
    def create_service(cls, klass):
        """ create and generate a service class using the parameters above """

        class BaseService:
            model_class = klass
            objects = klass.objects

            @classmethod
            def _prepare_id(cls, obj_id):
                """ Determine whether obj_id is of type ObjectId or not"""
                if not isinstance(obj_id, ObjectId) and ObjectId.is_valid(str(obj_id)):
                    obj_id = ObjectId(str(obj_id))

                return obj_id

            @classmethod
            def get(cls, obj_id):
                """ Get a single object from the database collection """

                if isinstance(obj_id, cls.model_class):
                    return obj_id

                _obj_id = obj_id
                obj_id = cls._prepare_id(obj_id)
                obj = cls.model_class.objects.get({"_id": obj_id})
                return obj

            @classmethod
            def find_one(cls, params):
                """ Find a single object that matches the criteria within the parameters """

                try:
                    obj = cls.model_class.objects.get(params)
                    return obj
                except klass.DoesNotExist:
                    print("Could not find any object that matches this criteria")
                    return
                except Exception as e:
                    print(e)
                    raise

            @classmethod
            def create(cls, ignored_args=None, **kwargs):
                """ base create method."""

                if not ignored_args:
                    ignored_args = ["_id", "date_created", "last_updated", "pk"]

                obj = cls.model_class()
                data = utils.clean_kwargs(ignored_args, kwargs)
                obj = utils.populate_obj(obj, data)

                try:
                    # print("===========>>>>did it save==========>>", obj)
                    obj = obj.save()
                    return obj
                except Exception as e:
                    print(e)
                    raise

            @classmethod
            def update(cls, obj_id, ignored_args=None, **kwargs):
                """ Update an existing record. if obj_id isn't an instance of ObjectId it will first be converted """

                if not ignored_args:
                    ignored_args = ["_id", "date_created", "last_updated", "pk"]

                obj = cls.get(obj_id)
                data = utils.clean_kwargs(ignored_args, kwargs)
                obj = utils.populate_obj(obj, data)
                if "last_updated" in ignored_args:
                    obj.last_updated = datetime.utcnow()
                try:
                    obj = obj.save()
                    return obj
                except Exception as e:
                    print(e)
                    raise

            @classmethod
            def delete(cls, obj_id):
                """ Delete object by id """

                obj = cls.get(obj_id)

                try:
                    obj.delete()
                    return obj
                except Exception as e:
                    print(e)
                    raise

        return BaseService
