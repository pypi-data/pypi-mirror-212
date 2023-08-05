from setuptools import setup, find_packages

setup(
    name='choclo-checker',
    version='1.0.1',
    description='Choclo checker',
    author='Julio César Herrán La Rosa',
    author_email='jherranlarosa@gmail.com',
    url='https://jherranlarosa.com',
    packages=find_packages(),
    install_requires=[
        'pymysql',
        'pymongo',
        'requests',
        'ping3',
        'psycopg2',
        'pyodbc',
        'boto3',
        'elasticsearch'
    ],
)
