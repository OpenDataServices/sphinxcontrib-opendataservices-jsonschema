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

TODO Document, with example of calling.

Option: collapse
----------------

TODO Document, with example of calling.

Option: pointer
---------------

You can pass the optional setting `pointer`.

.. code-block:: rst

    .. jsonschema:: ../_build_schema/components.json
       :pointer: /definitions/Address

You can use this to only show a section of the JSON Schema - in this case, only the section underneath `/definitions/Address` will be shown.


Option: nocrossref
------------------

TODO Document, with example of calling.
