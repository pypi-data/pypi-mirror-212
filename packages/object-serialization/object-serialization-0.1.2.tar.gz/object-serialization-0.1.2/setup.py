from setuptools import setup, find_packages

setup(
    name='object-serialization',
    version='0.1.2',
    description='Python serialization package for python objects',
    packages=find_packages(),
    install_requires=[],
    py_modules=['MySerializer', 'json_helper', 'serialization_helper', 'xml_helper'],
)
