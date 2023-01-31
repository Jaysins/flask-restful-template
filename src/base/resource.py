from flask_restful import Resource
from flask import request, make_response, abort
from marshmallow import EXCLUDE, ValidationError


class BaseResource(Resource):

    def __init__(self):
        """

        """

    def query(self):
        """this is the query that to the database"""
        return self.service_klass.objects

    def limit_query(self, query, **kwargs):
        """limit the results of a query to what want the user to see"""
        user_context = request.environ.get("user_context")
        user_id = user_context.get("id")
        raw_query = {"user_id": user_id}
        return query.raw(raw_query)

    def limit_get(self, obj, **kwargs):
        """limit the ability to view a singular object to the actual owner of the object"""

        model_owner_id = getattr(obj, "user_id", None)
        model_owner_pk = getattr(obj, "pk", None)
        user_context = request.environ.get("user_context")
        user_id = user_context.get("id")
        if (model_owner_id and str(model_owner_id) == user_id) or (model_owner_pk and str(model_owner_pk) == user_id):
            return obj
        return abort(401, {"desc": "unauthorized"})

    def fetch(self, obj_id):
        """
        a helper function that is to be used in on_get requests when only obj_id is provided

        :param obj_id: the id of the object to get
        """

        try:
            obj = self.service_klass.get(obj_id)
        except Exception as e:
            print(e)
            return abort(404, {"desc": "requested object does not exist"})
        return obj

    def save(self, data, user_context=None):
        """
        Saves information sent in by on_post request, where no object id is specified.

        :param data: the data to be saved.
        :param user_context: the data to be saved.
        :return: Object that was created
        """
        return self.service_klass.create(**data)

    def update(self, obj_id, data, user_context=None):
        """
        Saves information sent in by on_post request, where no object id is specified.

        :param obj_id: the data to be updated.
        :param data: the data to be updated.
        :param user_context: the data to be updated.
        :return: Object that was created
        """
        return self.service_klass.update(obj_id, **data)

    def get(self, obj_id=None):
        """

        :return:
        :rtype:
        """
        schema = self.serializers.get("response")

        if not obj_id:
            base_query = self.query()
            limited_query = self.limit_query(base_query)
            return {"data": schema().dump(limited_query, many=True)}
        obj = self.fetch(obj_id)
        if not obj:
            abort(409, {"desc": "requested resource doesn't exist"})
        return schema().dump(self.limit_get(obj))

    def post(self):
        """

        :return:
        :rtype:
        """
        serializer = self.serializers.get("default")

        try:
            validated_data = serializer().load(data=request.json, unknown=EXCLUDE)
        except ValidationError as e:

            return abort(409, e.messages)
        user_context = request.environ.get("user_context")

        resp = self.save(data=validated_data, user_context=user_context)
        resp_serializer = self.serializers.get("response")
        return resp_serializer().dump(resp)

    def put(self, obj_id=None):
        """

        :param obj_id:
        :type obj_id:
        :return:
        :rtype:
        """

        self.limit_get(self.fetch(obj_id))
        serializer = self.serializers.get("default")

        try:
            validated_data = serializer().load(data=request.json, unknown=EXCLUDE)
        except ValidationError as e:
            return abort(409, e.messages)
        user_context = request.environ.get("user_context")

        resp = self.update(obj_id=obj_id, data=validated_data, user_context=user_context)
        resp_serializer = self.serializers.get("response")
        return resp_serializer().dump(resp)

    def delete(self, obj_id=None):
        """

        :param obj_id:
        :type obj_id:
        :return:
        :rtype:
        """

        self.limit_get(self.fetch(obj_id))
        self.service_klass.update(obj_id, deleted=True)
        return {"status": "successful"}

    @classmethod
    def initiate(cls, serializers=None, service_klass=None):
        cls.serializers = serializers
        cls.service_klass = service_klass
        return cls
