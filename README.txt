collection-json
===============

.. image:: https://badge.fury.io/py/collection-json.png
    :target: http://badge.fury.io/py/collection-json

.. image:: https://travis-ci.org/ricardokirkner/collection-json.python.png?branch=master
    :target: https://travis-ci.org/ricardokirkner/collection-json.python

.. image:: https://coveralls.io/repos/ricardokirkner/collection-json.python/badge.png
    :target: https://coveralls.io/r/ricardokirkner/collection-json.python


collection-json is a small library, written in Python, to work with Collection+JSON documents.


Installation
------------

The easiest way to install `collection-json` is to run
::

    $ pip install collection-json


For other ways of installing it, please refer to the documentation_.


Examples
--------

Parsing a Collection+JSON document is really simple
::

    >>> import requests
    >>> from collection_json import Collection
    >>> data = requests.get('http://www.youtypeitwepostit.com/api/').text
    >>> collection = Collection.from_json(data)
    >>> collection
    <Collection: version='1.0' href='http://www.youtypeitwepostit.com/api/'>


The documentation_ includes several usage examples, go and check it out!


.. _documentation: http://collection-json.readthedocs.org
