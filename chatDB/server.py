import asyncio

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.routing import APIRouter
from chatDB.urls import urls
from common.init_yaml import yaml_data

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
router = APIRouter()


async def add_route():
    if len(urls) > 0:
        for _url in urls:
            route_path = _url[0]
            handler = _url[1]
            if len(_url) > 2:
                methods = _url[2]
            else:
                methods = ["GET", "POST"]
            router.add_api_route(route_path, handler, methods=methods)
            app.include_router(router)


if __name__ == '__main__':
    asyncio.run(add_route())
    host = yaml_data["server"]["host"]
    port = yaml_data["server"]["port"]
    uvicorn.run(app, host=host, port=port)
