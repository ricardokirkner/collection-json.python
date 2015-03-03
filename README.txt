collection-json
===============

.. image:: https://badge.fury.io/py/collection-json.png
    :target: http://badge.fury.io/py/collection-json

.. image:: https://travis-ci.org/ricardokirkner/collection-json.python.png?branch=master
    :target: https://travis-ci.org/ricardokirkner/collection-json.python

.. image:: https://coveralls.io/repos/ricardokirkner/collection-json.python/badge.png
    :target: https://coveralls.io/r/ricardokirkner/collection-json.python


collection-json is a small library, written in Python, to work with
Collection+JSON documents.


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


Contributing
------------

1. Check for open issues or open a fresh issue to start a discussion around a
   feature idea or a bug.
1. Fork `the repository`_ on GitHub to start making your changes to the
   **master** branch (or branch off of it).
1. Write a test which shows that the bug was fixed or that the feature works
   as expected.
1. Send a pull request and bug the maintainer until it gets merged and
   published. :) Make sure to add yourself to AUTHORS_.

.. _`the repository`: https://github.com/ricardokirkner/collection-json.python
.. _AUTHORS: https://github.com/ricardokirkner/collection-json.python/blob/master/AUTHORS.txt
