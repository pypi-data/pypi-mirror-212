import click
import os

@click.command('initializeproject')
@click.argument('project_name')
def startproject(project_name):
    """
    Create a new project with the given name.
    """
    # Create the project directory
    project_dir = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_dir, exist_ok=True)
    click.echo(f"Created project directory: {project_dir}")

    # Create additional directories
    directories = ['conf', 'src', 'src/core', 'src/config', 'src/logger']
    for directory in directories:
        directory_path = os.path.join(project_dir, directory)
        os.makedirs(directory_path, exist_ok=True)
        click.echo(f"Created directory: {directory_path}")


    # Create files
    files = {
        'main.py': '''import uvicorn
from utils import include_routers, init
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware


app = FastAPI(title="FANG - Made on Fast API", version="0.0.1")
include_routers(app)


@app.get("/")
def main_route():
    return "welcome to fang"

if __name__ == '__main__':
    init()
    uvicorn.run(app, host="127.0.0.1", port=5001)
        ''',
        'settings.py': '''from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DATABASES = {
    'default': {
        'ENGINE': 'sqlite',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}
        ''',
        'utils.py':'''import inspect
from pathlib import Path
from fastapi import FastAPI, APIRouter
from importlib import import_module
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from settings import DATABASES

def include_routers(app: FastAPI):
    """
    Discovers router modules in the app
    """
    routers_dir = Path("src/core")
    for router_file in routers_dir.rglob("router.py"):
        module_name = ".".join(router_file.with_suffix("").parts)
        module = import_module(module_name)
        router = getattr(module, "router", None)
        if isinstance(router, APIRouter):
            app.include_router(router)
def init():
    """
    Add functions that need to be run during program initialization
    """
    pass
        ''',
        'README.md':'# Project Documentation',
        'conf/__init__.py':'',
        'conf/env.conf':'',
        'src/__init__.py':'',
        'src/config/__init__.py':'',
        'src/config/config.py':'',
        'src/config/constants.py':'',
        'src/core/__init__.py':'',
        'src/logger/__init__.py':'',
    }
    for file_path, file_content in files.items():
        file_path = os.path.join(project_dir, file_path)
        with open(file_path, 'w') as file:
            file.write(file_content)
        click.echo(f"Created file: {file_path}")

    click.echo("Project initialized successfully.")

if __name__ == '__main__':
    startproject()
