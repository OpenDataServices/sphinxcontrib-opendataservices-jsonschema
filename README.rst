sphinxcontrib-opendataservices-jsonschema
=========================================

`sphinxcontrib-opendataservices-jsonschema` is Sphinx extension to define data structure using `JSON Schema`_

.. _JSON Schema: http://json-schema.org/

Usage
-----

Include this extension in conf.py::

    extensions = ['sphinxcontrib.jsonschema']

Write ``jsonschema`` directive into reST file where you want to import schema::

    .. jsonschema:: path/to/your.json


Docs
----

https://sphinxcontrib-opendataservices-jsonschema.readthedocs.io/en/latest/ , or see the docs folder in this repository

PyPi
----

Available at https://pypi.org/project/sphinxcontrib-opendataservices-jsonschema/

Don't install this package and https://pypi.org/project/sphinxcontrib-jsonschema/ at the same time, as they use the same Python namespace.

History
-------

This project was started as https://github.com/tk0miya/sphinxcontrib-jsonschema and forked by Open Data Services Co-operative in May 2020. Thanks to all the original authors.
