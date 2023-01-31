from src.resources.auth import RegisterResource, LoginResource
from src.resources.template import TemplateResource
from src.services.template import TemplateService
from src.services.user import UserService
from src.base.middleware import AuthMiddleware
import settings
from src import app, api

app.wsgi_app = AuthMiddleware(app.wsgi_app, settings=settings, ignored_endpoints=["/register", "/login"])


template = TemplateResource.initiate(serializers=TemplateResource.serializers, service_klass=TemplateService)
register = RegisterResource.initiate(serializers=RegisterResource.serializers, service_klass=UserService)
login = LoginResource.initiate(serializers=LoginResource.serializers, service_klass=UserService)


api.add_resource(register, '/register')
api.add_resource(login, '/login')
api.add_resource(template, '/template', '/template/<string:obj_id>')


if __name__ == '__main__':
    app.run(debug=True)