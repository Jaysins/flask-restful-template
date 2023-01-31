from flask import make_response, abort

from src.schema import RegistrationSchema, UserResponseSchema, LoginSchema, LoginResponseSchema
from src.base.resource import BaseResource


class RegisterResource(BaseResource):
    """

    """

    serializers = {"default": RegistrationSchema,
                   "response": UserResponseSchema}

    def get(self, obj_id=None):
        abort(400)

    def save(self, data, user_context=None):
        """

        :param data:
        :type data:
        :param user_context:
        :type user_context:
        :return:
        :rtype:
        """
        return self.service_klass.register_account(**data)


class LoginResource(BaseResource):
    serializers = {
        "default": LoginSchema,
        "response": LoginResponseSchema
    }

    def get(self, obj_id=None):
        abort(400)

    def save(self, data, user_context=None):
        """

        :param data:
        :type data:
        :param user_context:
        :type user_context:
        :return:
        :rtype:
        """
        email = data.get("email")
        user = self.service_klass.find_one({"email": email})

        if not user.check_password(data.get("password")):
            abort(409, {"err": "invalid password supplied"})
        return user
