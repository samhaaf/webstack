from chalice import ConvertToMiddleware
from .sessions import inject_session
from .responses import format_response

# all_middleware = [inject_session]


def register_middleware(blueprint, middleware=None):
    if middleware is None:
        return lambda middleware: register_middleware(blueprint, middleware)

    middleware.blueprint = blueprint
    blueprint.register_middleware(ConvertToMiddleware(middleware))

# def register_all_middleware(blueprint):
#     for middleware in all_middleware:
#         register_middleware(blueprint, middleware)
