from marshmallow import Schema, EXCLUDE, fields as _fields, validates, ValidationError

from src.models import User


class ExcludeSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class UserResponseSchema(ExcludeSchema):
    pk = _fields.String(required=False, allow_none=True)
    date_created = _fields.DateTime(required=False, allow_none=True)
    first_name = _fields.String(required=True, allow_none=False)
    last_name = _fields.String(required=True, allow_none=False)
    email = _fields.String(required=True, allow_none=False)


class RegistrationSchema(UserResponseSchema):
    password = _fields.String(required=True, allow_none=False)


class LoginSchema(ExcludeSchema):
    password = _fields.String(required=True, allow_none=False)
    email = _fields.String(required=True, allow_none=False)

    @validates("email")
    def validate_email(self, email):
        if not User.objects.raw({"email": email}).count():
            raise ValidationError(message="Invalid email", field_name="email")


class LoginResponseSchema(UserResponseSchema):
    auth_token = _fields.String(required=True, allow_none=False)


class TemplateSchema(ExcludeSchema):
    """ Model for storing information about an entity or user who owns an account or set of accounts.
    _id will be equivalent to either the user_id or the entity_id
    """

    template_name = _fields.String(required=True, allow_none=False)
    body = _fields.String(required=True, allow_none=False)
    subject = _fields.String(required=True, allow_none=False)


class TemplateResponseSchema(TemplateSchema):
    pk = _fields.String(required=False, allow_none=True)
    user_id = _fields.String(required=False, allow_none=True)
    date_created = _fields.DateTime(required=True, allow_none=False)
    last_updated = _fields.DateTime(required=True, allow_none=False)
