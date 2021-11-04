Examples
========


Schema files for these examples
-------------------------------

You can see the schema files used for these examples:

* `example_schema.json <example_schema.json>`_
* `example_schema_with_external_refs.json <example_schema_with_external_refs.json>`_
* `example_components.json <example_components.json>`_

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

With externallinks option
-------------------------

.. code-block:: rst

    .. jsonschema:: example_schema.json
       :include: formalname
       :externallinks: {"formalname":{"url":"https://en.wikipedia.org/wiki/Butler","text":"A guide on how to use formal names"}}

.. jsonschema:: example_schema.json
   :include: formalname
   :externallinks: {"formalname":{"url":"https://en.wikipedia.org/wiki/Butler","text":"A guide on how to use formal names"}}

With allowexternalrefs option
-----------------------------

.. code-block:: rst

    .. jsonschema:: example_schema_with_external_refs.json
       :allowexternalrefs:

.. jsonschema:: example_schema_with_external_refs.json
   :allowexternalrefs:
