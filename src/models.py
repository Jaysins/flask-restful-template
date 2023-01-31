"""
models.py

Data model file for application. This will connect to the mongo database and provide a source for storage
for the application service

"""

import settings
import pymongo

from pymongo.write_concern import WriteConcern
from pymongo.operations import IndexModel
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from datetime import datetime, timedelta
import bcrypt
import json
import jwt

# Must always be run before any other database calls can follow

connect(settings.MONGO_DB_URI, connect=False, maxPoolSize=None)


class AppMixin:
    """ App mixin will hold special methods and field parameters to map to all model classes"""

    def to_dict(self, exclude=None, do_dump=False):
        """

        @param exclude:
        @param do_dump:
        @return:
        """
        if isinstance(self, (MongoModel, EmbeddedMongoModel)):
            d = self.to_custom_son(exclude=exclude).to_dict()
            # [d.pop(i, None) for i in exclude]
            return json.loads(json.dumps(d, default=str)) if do_dump else d
        return self.__dict__


class User(MongoModel, AppMixin):
    """ Model for storing information about an entity or user who owns an account or set of accounts.
    _id will be equivalent to either the user_id or the entity_id
    """

    email = fields.CharField(required=False, blank=True)
    first_name = fields.CharField(required=False, blank=True)
    password = fields.CharField(required=False, blank=True)
    last_name = fields.CharField(required=False, blank=True)
    date_created = fields.DateTimeField(required=True, blank=False, default=datetime.utcnow)
    last_updated = fields.DateTimeField(required=True, blank=False, default=datetime.utcnow)

    class Meta:
        """
        Meta class
        """

        write_concern = WriteConcern(j=True)
        ignore_unknown_fields = True
        indexes = [
            IndexModel([("_cls", pymongo.DESCENDING), ("email", pymongo.ASCENDING), ("first_name", pymongo.ASCENDING),
                        ("last_name", pymongo.ASCENDING), ("date_created", pymongo.DESCENDING), ])]

    def set_password(self, password):
        """
        Password hashing logic for each model.
        This will be run on every user object when it is created.

        Arguments:
            password {str or unidecode} -- The password, in clear text, to be hashed and set on the model
        """

        if not password or not isinstance(password, (str, bytes)):
            raise ValueError("Password must be non-empty string or bytes value")

        self.password = (bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())).decode()
        # set last updated.
        self.last_updated = datetime.utcnow()

        return self.save()

    def check_password(self, password):
        """
        Password checking logic.
        This will be used whenever a user attempts to authenticate.

        Arguments:
            password {str or bytes} -- The password to be compared, in clear text.

        Raises:
            ValueError -- Raised if there is an empty value in password

        Returns:
            bool -- True if password is equal to hashed password, False if not.
        """

        if not password or not isinstance(password, (str, bytes)):
            raise ValueError("Password must be non-empty string or bytes value")

        # both password and hashed password need to be encrypted.
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    @property
    def auth_token(self):
        """ Generate the auth token for this user from the current data embedded within the application """

        if not self.pk:
            raise ValueError("Cannot generate token for unsaved object")

        expires_in = datetime.now() + timedelta(hours=int(settings.JWT_EXPIRES_IN_HOURS))

        payload = dict(first_name=self.first_name, last_name=self.last_name, id=str(self.pk), exp=expires_in)
        # print(payload, "token the payload")
        encoded = jwt.encode(payload, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded


class Template(MongoModel, AppMixin):
    """ Model for storing information about an entity or user who owns an account or set of accounts.
    _id will be equivalent to either the user_id or the entity_id
    """

    name = fields.CharField(required=False, blank=True)
    body = fields.CharField(required=False, blank=True)
    user_id = fields.CharField(required=False, blank=True)
    subject = fields.CharField(required=False, blank=True)
    deleted = fields.BooleanField(required=False, default=False)
    date_created = fields.DateTimeField(required=True, blank=False, default=datetime.utcnow)
    last_updated = fields.DateTimeField(required=True, blank=False, default=datetime.utcnow)

    class Meta:
        """
        Meta class
        """

        write_concern = WriteConcern(j=True)
        ignore_unknown_fields = True
        indexes = [
            IndexModel([("_cls", pymongo.DESCENDING), ("deleted", pymongo.ASCENDING), ("subject", pymongo.ASCENDING),
                        ("date_created", pymongo.DESCENDING), ])]
