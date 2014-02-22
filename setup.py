try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import collection_json


classifiers = [
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities',
]


setup(
    name='collection-json',
    version=collection_json.__version__,
    author='Ricardo Kirkner',
    author_email='ricardo@kirkner.com.ar',
    url='http://pypi.python.org/pypi/collection-json',
    py_modules=['collection_json'],
    description='Small library to work with Collection+JSON documents.',
    long_description=open('README.txt').read(),
    license='BSD',
    classifiers=classifiers,
)
