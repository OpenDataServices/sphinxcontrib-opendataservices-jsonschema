Examples
========

Basic Example
-------------

.. code-block:: rst

    .. jsonschema:: example_schema.json

.. jsonschema:: example_schema.json



With include option
-------------------

.. code-block:: rst

    .. jsonschema:: example_schema.json
       :include: id,name,age/actual

.. jsonschema:: example_schema.json
   :include: id,name,age/actual


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

