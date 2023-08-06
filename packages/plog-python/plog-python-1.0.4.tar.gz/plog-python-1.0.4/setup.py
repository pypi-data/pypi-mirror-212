from setuptools import setup, find_packages

setup(
    name='plog-python',
    version='1.0.4',
    description='A service for logging data and objects in different steps of applications',
    long_description='A service for logging data and objects in different steps of applications',
    author='Ali Khodadoost',
    author_email='ali1.khodadoost@gmail.com',
    license='MIT',
    packages=find_packages("."),
    install_requires=[
        'pandas',
        'python-dateutil',
        'python-multipart',
        'sqlmodel',
    ],
)