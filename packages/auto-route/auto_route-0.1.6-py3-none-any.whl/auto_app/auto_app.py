import importlib
import logging
import os
import sys
from typing import List, Optional

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel



class InitClassObject(BaseModel):
    class_name: str
    init_args: Optional[dict] = None


class AutoLoadRouterConfigObject(BaseModel):
    module_path: str
    router_names: List[str]

    # Classes to instantiate
    init_classes: Optional[List[InitClassObject]] = None


class APIAutoApp:
    def __init__(self, routers_list: List[APIRouter and str] = None):
        self.routers_list = routers_list

    def load_routers_to_app(self, app: FastAPI, routers) -> None:

        for router in routers:
            from auto_route.auto_route import APIAutoRouter
            if isinstance(router, AutoLoadRouterConfigObject):
                # fixme relative paths
                module_path = router.module_path.replace(".py", "").replace("/", ".")
                current_dir = os.path.dirname(__file__)
                parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
                # path_to_add = os.path.abspath(os.path.join(current_dir, module_path))
                sys.path.insert(0, parent_dir)

                module = importlib.import_module(module_path, package=".")
                for router_name in router.router_names:
                    custom_api_router = getattr(module, router_name)
                    app.include_router(router=custom_api_router.router)
                #
                # Init classes if any
                if router.init_classes is not None:  # This is so fucking stupid to-do
                    assert isinstance(router.init_classes[0], InitClassObject), "init_class_names must be a list"
                    for iclass in router.init_classes:
                        service_class = getattr(module, iclass.class_name)
                        service_instance = service_class(**(iclass.init_args or {}))
                        logging.debug(f"Initialized {iclass.class_name} as {service_instance}")
            #
            #
            elif isinstance(router, APIRouter or APIAutoRouter):
                app.include_router(router=router)
            else:
                print(
                    f'Router input {router} is not a valid type expected for routes. Either AutoLoadRouterConfigObject or APIRouter')

    def build_app(self, settings: dict = None) -> FastAPI:
        if settings is None:
            settings = {}
        app = FastAPI(**settings)

        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.get('allow_origins', ["*"]),
            allow_credentials=settings.get('allow_credentials', True),
            allow_methods=settings.get('allow_methods', ["*"]),
            allow_headers=settings.get('allow_headers', ["*"]),
        )

        self.load_routers_to_app(app, self.routers_list)
        return app

    def run(self, host: str = "0.0.0.0", port: int = 8000, app: FastAPI = None, **kwargs) -> None:
        if app is None:
            app = self.build_app()
        import uvicorn
        uvicorn.run(app, host=host, port=port, **kwargs)


if __name__ == '__main__':
    stripe_router_config = AutoLoadRouterConfigObject(
        module_path='Stripe/stripe_class.py',
        router_names=['stripe_router'],
        init_classes=[
            InitClassObject(class_name='Customer'),
            InitClassObject(class_name='Payment_Intent'),
            InitClassObject(class_name='Subscriptions'),
        ]
    )

    apiautoapp = APIAutoApp(routers_list=[stripe_router_config])

    app = apiautoapp.build_app()
    apiautoapp.run(host='localhost', port=8000, app=app)
