from bson import ObjectId
from flask import abort

from src.base.resource import BaseResource
from src.schema import TemplateSchema, TemplateResponseSchema


class TemplateResource(BaseResource):
    """

    """

    serializers = {
        "default": TemplateSchema,
        "response": TemplateResponseSchema
    }

    def query(self):
        """

        :return:
        :rtype:
        """
        return self.service_klass.objects.raw({"deleted": False})

    def fetch(self, obj_id):
        """

        :param obj_id:
        :type obj_id:
        :return:
        :rtype:
        """
        obj = self.service_klass.find_one({"_id": ObjectId(obj_id), "deleted": False})
        return obj

    def save(self, data, user_context=None):
        """

        :param data:
        :type data:
        :param user_context:
        :type user_context:
        :return:
        :rtype:
        """
        data["user_id"] = user_context.get("id")
        data["name"] = data.pop("template_name")
        return self.service_klass.create(**data)
