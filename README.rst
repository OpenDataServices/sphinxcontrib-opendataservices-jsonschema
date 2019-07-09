sphinxcontrib-jsonschema
========================

`sphinxcontrib-jsonschema` is Sphinx extension to define data structure using `JSON Schema`_

.. _JSON Schema: http://json-schema.org/

Usage
-----

Include this extension in conf.py::

    extensions = ['sphinxcontrib.jsonschema']

Write ``jsonschema`` directive into reST file where you want to import schema::

    .. jsonschema:: path/to/your.json

Option - pointer
----------------

To be documented


Option - include
-----------------


To be documented


Option - collapse
-----------------


To be documented

Option - externallinks
----------------------

After some entries, it will generate a "See" link.

This will happen automatically every time there is a JSON reference.

You can also tell it to happen explicitly on certain nodes, by use of the externallinks option.

        :externallinks: {"share":{"url":"#share","text":"Share"},"unspecified/reason":{"url":"https://www.google.com/","text":"Google"}}

The first key is the name of the property to add the link to. Note you can do paths.

The url is the url to link to, and the text is what is shown on in the link, after "See".


Option - nocrossref
-------------------

After some entries, it will generate a "See" link.

This will happen automatically every time there is a JSON reference.

If you do not want this behavior, pass this flag.
