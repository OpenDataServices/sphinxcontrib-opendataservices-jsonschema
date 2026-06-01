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


Option: prefix
--------------

You can pass the optional setting `prefix`.

.. code-block:: rst

    .. jsonschema:: example_schema.json
       :prefix: myprefix

If passed, the value is prepended to the HTML anchor ID generated for each property. Without a prefix the anchor ID is formed from the filename, the pointer (if set), and the property path — for example ``test.json,,name``. With ``:prefix: myprefix`` it becomes ``myprefix,test.json,,name``.

This is useful when the same schema is included more than once in a documentation site, where duplicate anchor IDs would otherwise cause conflicts.

Option: addtargets
------------------

You can pass the optional flag `addtargets`.

.. code-block:: rst

    .. jsonschema:: example_schema.json
       :addtargets:

If passed, each property's anchor is registered with Sphinx's cross-reference system, making it referenceable from other pages using the ``:ref:`` role. Without this flag the anchor IDs still appear in the HTML (so ``#anchor`` links work within the same page), but Sphinx does not know about them.

If the same schema is included on multiple pages, use ``:prefix:`` alongside ``:addtargets:`` to keep anchor IDs unique and avoid duplicate target warnings.

Option: pointer
---------------

You can pass the optional setting `pointer`.

.. code-block:: rst

    .. jsonschema:: example_schema.json
       :pointer: /properties/address

You can use this to only show a section of the JSON Schema - in this case, only the section underneath `/properties/address` will be shown.

Note the key here is the key is the key in the JSON Schema not the key in the JSON data. This means you can pass keys like `/definitions/Address`.

Option: collapseonref
---------------------

You can pass the optional flag `collapseonref`.

.. code-block:: rst

    .. jsonschema:: example_schema.json
       :collapseonref:

If passed, any property that uses ``$ref`` will be collapsed — its child properties will not be shown. This is useful when definitions are documented separately and you want to avoid duplicating their fields inline.

This is equivalent to listing every ``$ref`` property path in the ``collapse`` option, but updates automatically when the schema changes.

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
