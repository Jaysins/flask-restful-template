from werkzeug.wrappers import Request, Response
import jwt


class AuthMiddleware(object):
    '''
    Simple WSGI middleware
    '''

    def __init__(self, app, settings, ignored_endpoints=None):
        self.app = app
        self.ignored_endpoints = ignored_endpoints
        self.settings = settings

    def __call__(self, environ, start_response):

        request = Request(environ)
        user_context = self.validate_token(token=request.headers.get("Authorization", None))
        if not user_context and not self.check_ignored_endpoints(path=request.path):
            res = Response("Authorization failed", content_type='application/json', status=401)
            return res(environ, start_response)

        environ['user_context'] = user_context
        return self.app(environ, start_response)

    def validate_token(self, token):
        """

        :param token:
        :type token:
        :return:
        :rtype:
        """
        try:
            token = token.split("Bearer ")[1]
            data = jwt.decode(token, self.settings.JWT_SECRET_KEY, algorithms=self.settings.JWT_ALGORITHM)
            return data
        except Exception as e:
            print(e)
        return None

    def check_ignored_endpoints(self, path, base_path=''):
        """separate possible base api endpoints """

        if base_path is None:
            base_path = ""
        if not self.ignored_endpoints:
            return

        stripped = path.strip(base_path)
        relative_path = "/" + path.strip(base_path)
        if stripped.startswith('/'):
            relative_path = stripped
        for i in self.ignored_endpoints:
            if not i.startswith("/"):
                i = "/" + i
            l = len(i)
            if i[:] == relative_path[:l]:
                return True
        return False
