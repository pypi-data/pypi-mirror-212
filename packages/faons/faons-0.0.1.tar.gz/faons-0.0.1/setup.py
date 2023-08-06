from setuptools import setup, find_packages

setup(
    name='faons',
    version='0.0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'faons = faons.cli:startproject'
        ]
    },
    install_requires=[
        'click',
        'SQLAlchemy',
        'sqlalchemy_utils',
        'uvicorn',
        'fastapi',
        'db-sqlite3',

    ],
)
