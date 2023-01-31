from ..base.service import ServiceFactory
from ..models import User
from pprint import pprint


BaseUserService = ServiceFactory.create_service(User)


class UserService(BaseUserService):
    """

    """

    @classmethod
    def register_account(cls, **kwargs):
        """

        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        pprint(kwargs)
        password = kwargs.pop("password")
        user = cls.create(**kwargs)
        return user.set_password(password)
