import ast
import re
from setuptools import setup, find_packages

# get __version__ in __init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('jsonls/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

# load README.rst
with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name="jsonls",
    version=version,
    url="https://github.com/json-transformations/jsonls",
    keywords=[],

    author="Brian Peterson",
    author_email="bpeterso2000@yahoo.com",

    description="A tool to explore and list JSON data",
    long_description=readme,

    packages=find_packages(include=['jsonls']),
    include_package_data=True,
    zipsafe=False,

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    install_requires=[
        'jsoncore==0.6.1'
    ],
    test_suite='tests',
    test_requires=[
        'flake8',
        'pytest-cov',
        'tox'
    ],
    setup_requires=['pytest-runner'],
    entry_points={
        'console_scripts': [
            'jsonls=jsonls.cli:main'
        ]
    },

)
