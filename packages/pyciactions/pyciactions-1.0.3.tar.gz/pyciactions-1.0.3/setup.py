from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='pyciactions',
    version='1.0.3',
    description='Declarative builder for Github Action Scripts',
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='Julien Bongars',
    packages=['pyciactions'],
    install_requires=[
        "dataclasses==0.6",
        "PyYAML==6.0"
    ],
    url='https://github.com/JBongars/pyciactions',
)
