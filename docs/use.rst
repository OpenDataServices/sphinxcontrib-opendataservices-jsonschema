Use
===

This provides a single directive, `jsonschema`:

.. code-block:: rst

    .. jsonschema:: ../_build_schema/components.json

Required: Path to the JSON Schema file
--------------------------------------

You must pass the path to the JSON Schema file to the widget.

.. code-block:: rst

    .. jsonschema:: ../_build_schema/components.json

Option: include
---------------

You can pass the optional setting `include`.

.. code-block:: rst

    .. jsonschema:: example_schema.json
       :include: id,name,age/actual

Only the keys listed will be shown.


Option: collapse
----------------


You can pass the optional setting `collapse`.

.. code-block:: rst

    .. jsonschema:: example_schema.json
       :collapse: age

If passed, then any schema below the passed key will not be shown.


Option: pointer
---------------

You can pass the optional setting `pointer`.

.. code-block:: rst

    .. jsonschema:: example_schema.json
       :pointer: /properties/address

You can use this to only show a section of the JSON Schema - in this case, only the section underneath `/properties/address` will be shown.

Note the key here is the key is the key in the JSON Schema not the key in the JSON data. This means you can pass keys like `/definitions/Address`.

Option: nocrossref
------------------

You can pass the optional flag `nocrossref`.


.. code-block:: rst

    .. jsonschema:: example_schema.json
       :nocrossref:

By default, if an item has a `$ref` property then some text will be added to the Description with a link to a HTML anchor.

If you don't want this, pass this flag to disable this.

Option: externallinks
---------------------

You can pass a dictionary of dictionaries to this.

.. code-block:: rst

    .. jsonschema:: example_schema.json
       :externallinks: {"formalname":{"url":"https://en.wikipedia.org/wiki/Butler","text":"A guide on how to use formal names"}}


For every property included, a extra link will be included with the URL and text specified in the description section.


Option: allowexternalrefs
-------------------------

You can pass the optional flag `allowexternalrefs`.

.. code-block:: rst

    .. jsonschema:: example_schema_with_external_refs.json
       :allowexternalrefs:

If passed, you can use `$ref` to load remote files and they will be loaded.

If not passed, any remote references will silently be ignored.
