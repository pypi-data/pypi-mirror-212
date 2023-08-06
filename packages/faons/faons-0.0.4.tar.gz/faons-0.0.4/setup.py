from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='faons',
    version='0.0.4',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'faons = faons.cli:faons'
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
