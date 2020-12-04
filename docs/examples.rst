Examples
========

Basic Example
-------------

.. code-block:: rst

    .. jsonschema:: example_schema.json

.. jsonschema:: example_schema.json


With collapse option
--------------------

.. code-block:: rst

    .. jsonschema:: example_schema.json
       :collapse: age

.. jsonschema:: example_schema.json
   :collapse: age


With pointer option
--------------------

.. code-block:: rst

    .. jsonschema:: example_schema.json
       :pointer: /definitions/Address

.. jsonschema:: example_schema.json
   :pointer: /definitions/Address


With nocrossref flag
--------------------

.. code-block:: rst

    .. jsonschema:: example_schema.json
       :nocrossref:

.. jsonschema:: example_schema.json
   :nocrossref:

