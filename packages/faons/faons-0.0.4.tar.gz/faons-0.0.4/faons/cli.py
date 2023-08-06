import click
import os
import sys
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from importlib import import_module
from sqlalchemy.exc import OperationalError
from inspect import isclass

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def faons():
    """
    Faons CLI tool for project creation.
    """
    pass

@click.command('initializeproject')
@click.argument('project_name')
def initializeproject(project_name):
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


app = FastAPI(title="FAONS - Made on Fast API", version="0.0.4")
include_routers(app)


@app.get("/")
def main_route():
    return "Welcome to FAONS"

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

@click.command('startapp')
@click.argument('app_name')
@click.option('--project-dir', help='Path to the project directory', type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
def startapp(app_name, project_dir):
    """
    Create a new app with the given name.
    """
    if project_dir is None:
        project_dir = os.getcwd()
    else:
        project_dir = os.path.abspath(project_dir)

    if not os.path.exists(project_dir):
        click.echo(f"Project directory does not exist: {project_dir}")
        return

    project_core_dir = os.path.join(project_dir, 'src/core')
    if not os.path.exists(project_core_dir):
        click.echo("The 'startapp' command can only be executed within a project directory created by 'initializeproject'.")
        return

    # Create additional directories
    directories = [os.path.join(project_core_dir, app_name)]
    for directory in directories:
        directory_path = os.path.join(project_dir, directory)
        os.makedirs(directory_path, exist_ok=True)
        click.echo(f"Created app: {directory_path}")

    # Create files
    files = {
        os.path.join(project_core_dir, app_name, '__init__.py'): '',
        os.path.join(project_core_dir, app_name, 'handler.py'): '# Define the logic for your router in this file',
        os.path.join(project_core_dir, app_name, 'models.py'): '''from pydantic import BaseModel

# Define your models below this line
        ''',
        os.path.join(project_core_dir, app_name, 'router.py'):f'''from fastapi import APIRouter, Response

router = APIRouter()

# Define your endpoints below this line. We have already created one for you

@router.get("/{app_name}")
def {app_name}():
    return "This is your first endpoint from {app_name} app"
        ''',
        os.path.join(project_core_dir, app_name, 'schema.py'):'# Define the tables for your app in this file',
        os.path.join(project_core_dir, app_name, 'utils.py'):'# Define the utilities for your app in this file',
    }
    for file_path, file_content in files.items():
        file_path = os.path.join(project_dir, file_path)
        with open(file_path, 'w') as file:
            file.write(file_content)

    click.echo("App created successfully.")

def import_schemas(project_dir):
    schemas = []
    src_path = os.path.join(project_dir, 'src', 'core')
    
    for root, dirs, files in os.walk(src_path):
        for file in files:
            if file == 'schema.py':
                path = os.path.join(root, file)
                module_name = os.path.splitext(os.path.basename(path))[0]
                sys.path.insert(0, root)
                module = import_module(module_name)
                schemas.append(module)
                sys.path.pop(0)
    
    return schemas

@click.command('updateschema')
@click.option('--project-dir', help='Path to the project directory', type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
def updateschema(project_dir):
    """
    Update the database schema by creating or altering tables.
    """
    if project_dir is None:
        project_dir = os.getcwd()
    else:
        project_dir = os.path.abspath(project_dir)

    if not os.path.exists(project_dir):
        click.echo(f"Project directory does not exist: {project_dir}")
        return

    settings_path = os.path.join(project_dir, 'settings.py')

    # Read settings from the module
    settings = {}
    with open(settings_path, 'r') as f:
        exec(f.read(), settings, {'__file__': settings_path})
    settings = {}
    exec_globals = {'__file__': os.path.abspath(settings_path)}
    exec(open(settings_path).read(), exec_globals, settings)

    # Get the db_url from the settings
    db_url = f"{settings['DATABASES']['default']['ENGINE']}:///{settings['DATABASES']['default']['NAME']}"
    engine = create_engine(db_url)

    # Define the create_or_alter_tables function here
    def create_or_alter_tables(engine):
        Session = sessionmaker(bind=engine)
        session = Session()

        schemas = import_schemas(project_dir)
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        # Remove tables that no longer exist in the schema
        for table_name in existing_tables:
            if not any(
                issubclass(obj, schema.Base) and obj is not schema.Base and hasattr(obj, '__tablename__') and obj.__tablename__ == table_name
                for schema in schemas
                for name, obj in schema.__dict__.items()
                if isclass(obj)
            ):
                with engine.connect() as connection:
                    connection.execute(text(f'DROP TABLE "{table_name}"'))
                print(f"Table '{table_name}' removed.")

        # Create or alter tables
        for schema in schemas:
            for name, obj in schema.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, schema.Base) and obj is not schema.Base:
                    if hasattr(obj, '__tablename__'):
                        table_name = obj.__tablename__

                        if inspector.has_table(table_name):
                            # Table already exists, check for columns to add or modify
                            existing_columns = inspector.get_columns(table_name)
                            schema_columns = obj.__table__.columns

                            # Check if any new columns need to be added
                            for column in schema_columns:
                                if column.name not in [c['name'] for c in existing_columns]:
                                    column_name = column.name
                                    column_type = column.type
                                    with engine.connect() as connection:
                                        connection.execute(text(f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" {column_type}'))
                                    print(f"Table '{table_name}' altered. Column '{column_name}' added.")

                            # Check if any columns need to be modified
                            for column in existing_columns:
                                if column['name'] not in [c.name for c in schema_columns]:
                                    column_name = column['name']
                                    with engine.connect() as connection:
                                        connection.execute(text(f'ALTER TABLE "{table_name}" DROP COLUMN "{column_name}"'))
                                    print(f"Table '{table_name}' altered. Column '{column_name}' dropped.")

                        else:
                            # Table does not exist, create it
                            obj.metadata.create_all(engine)
                            print(f"Table '{table_name}' created.")

        session.close()

    # Call the create_or_alter_tables function
    create_or_alter_tables(engine)

    click.echo("Database schema updated successfully.")

    
faons.add_command(initializeproject)
faons.add_command(startapp)
faons.add_command(updateschema)

if __name__ == '__main__':
    faons()
