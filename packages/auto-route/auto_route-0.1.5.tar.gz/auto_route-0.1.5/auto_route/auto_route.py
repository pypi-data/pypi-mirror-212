import logging
from typing import TypeVar, Any, Optional, List, Callable, Dict, Tuple

from fastapi import APIRouter, status
from pydantic import BaseModel

logger = logging.getLogger(__name__)
T = TypeVar('T')


# Custom Exceptions
class RouteException(Exception):
    pass


class UnsupportedMethod(RouteException):
    pass


class PathConflict(RouteException):
    pass


class AutoRouteManager:
    _instance = None
    registered_paths = set()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.registered_paths = set()
        return cls._instance


def get_default_path_and_method(function: Callable, methods: str, keyword_mapping: Dict[str, str]) -> Tuple[str, str]:
    """
    Generate a default path for a given function and mapped keywords.

    The function name is split on underscores, and each part is checked against the mapped keywords. If a match is found,
    the part is replaced with a placeholder using the keyword.

    Args:
        function: The function for which the path is to be generated.
        methods: The default HTTP method if not provided explicitly.
        keyword_mapping: A dictionary of keywords to placeholders.

    Returns:
        The generated path as a string and the extracted method as a string.
    """

    HTTP_METHODS_AVAILABLE = ['get', 'post', 'put', 'delete', 'options', 'head', 'patch', 'trace']
    logger.debug(f'{function.__name__ = }')
    path_parts = function.__name__.split('_')

    method_place_holder = path_parts[0].lower() in ['get', 'post', 'put', 'delete', 'options', 'head', 'patch',
                                                    'trace']

    if methods:
        default_method = methods[0].lower()
        if method_place_holder and path_parts[0].lower() != default_method:
            logger.warning(f"The function name suggests the HTTP method {path_parts[0].upper()}, "
                           f"but the passed method is {methods[0].upper()}. "
                           f"Consider changing the function name to match the method for clarity.")
    else:
        assert len(path_parts) > 0, "Function name must be at least one character long."
        assert path_parts[0].lower() in HTTP_METHODS_AVAILABLE, \
            f"Function name must start with a valid HTTP method. " \
            f"Valid methods are: {HTTP_METHODS_AVAILABLE}"
        default_method = path_parts[0].lower()

    path_parts = path_parts if not method_place_holder else path_parts[1:]
    for i, part in enumerate(path_parts):
        if part in keyword_mapping:
            path_parts[i] = "{" + keyword_mapping[part] + "}"

    generated_default_path = f"/{default_method}/{'/'.join(path_parts)}"

    logger.debug(f'generated_default_path: {generated_default_path}')
    logger.debug(f'default_method: {default_method}')
    logger.debug(f'path_parts: {path_parts}')
    logger.debug(f'methods: {methods}')

    # exit()
    return generated_default_path, default_method


def check_path(path: str, override: bool) -> None:
    registered_paths = AutoRouteManager()._instance.registered_paths
    if not override and path in registered_paths:
        raise PathConflict(f"Path {path} is already registered. To override, set `override=True`."
                           f"The current Registered Paths are: {registered_paths}")
    registered_paths.add(path)


def route_functions_in_class(cls, router: APIRouter, prefix: str, tags: List[str]) -> None:
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value) and hasattr(attr_value, '_auto_route'):
            path, kwargs = attr_value._auto_route
            for method in kwargs.pop('methods'):
                route_decorator = getattr(router, method.lower(), None)
                if route_decorator is None:
                    raise UnsupportedMethod(f"Unsupported HTTP method: {method}")
                if tags:
                    kwargs['tags'] = kwargs.get('tags', []) + tags
                if prefix:
                    print(f'prefix: {prefix}')
                    path = f"{prefix.rstrip('/')}{path}"
                route_decorator(path, **kwargs)(attr_value)


def auto_route(
        path: Optional[str] = None,
        response_model: Optional[TypeVar] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        status_code: Optional[int] = status.HTTP_200_OK,
        operation_id: Optional[str] = None,
        summary: Optional[str] = None,
        override: Optional[bool] = False,
        mapped_keywords: Optional[dict] = None,
        **kwargs: Any,
) -> Callable[..., T]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        nonlocal path, response_model, description, tags, status_code, operation_id, override, mapped_keywords, summary

        mapped_keywords = mapped_keywords or {}
        path, method = get_default_path_and_method(func, kwargs.pop('methods', None), mapped_keywords)
        check_path(path, override)

        func._auto_route = (path, {
            'response_model': response_model or func.__annotations__.get('return'),
            'description': description or func.__doc__,
            'tags': tags or [],
            'status_code': status_code,
            'operation_id': operation_id or func.__name__,
            'summary': summary or func.__name__.replace('_', ' ').title(),
            'methods': [method],
            **kwargs,
        })

        # return staticmethod(func)
        return func

    return decorator


def register_router(router: APIRouter, prefix: str = '', tags: List[str] = []):
    def decorator(cls):
        nonlocal tags
        if not tags:
            tags = [cls.__name__.replace('_', ' ')]
        route_functions_in_class(cls, router, prefix, tags)
        return cls

    return decorator


class APIAutoRouter:
    def __init__(self):
        self.router = APIRouter()

    def route(self, *args, **kwargs):
        return auto_route(*args, **kwargs)

    def register(self, prefix: str = '', tags: List[str] = []):
        return register_router(self.router, prefix, tags)

    @staticmethod
    def retrieve_from_env(api_key_name):
        # if not available in environment variables, use the .env file
        import os
        if not os.environ.get(api_key_name):
            from dotenv import load_dotenv
            load_dotenv()
        return os.environ.get(api_key_name)


if __name__ == '__main__':
    api = APIAutoRouter()


    class User(BaseModel):
        id: int
        name: str


    @api.register()
    class User_Controller:
        @api.route()
        def get_user_by_id(id: int):
            return {"id": id, "name": "User"}

        @api.route()
        def post_user_by_id(user: User):
            return {"id": user.id, "name": user.name}

        @api.route()
        def delete_user_by_id(id: int):
            return {"id_deleted": id}


    from auto_app import APIAutoApp

    APIAutoApp(routers_list=[api.router]).run(host='localhost', port=8000)
