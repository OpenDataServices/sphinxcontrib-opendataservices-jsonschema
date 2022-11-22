Test with and without components - allow external refs!

We want to test the external schema is put in correctly.

.. jsonschema:: subdir/test-with-and-without-compontent.json
   :allowexternalrefs:





Test with and without components - do NOT allow external refs!

We just want to make sure it does not crash, and the output is as sensible as possible.

.. comment: jsonschema:: subdir/test-with-and-without-compontent.json

We can not test this example.

If external refs are not allowed {} is put in the de-referenced schema.
Then we get a crash:  can not find /definitions/pet in {}

See https://github.com/OpenDataServices/sphinxcontrib-opendataservices-jsonschema/issues/44





Test without components - allow external refs!

We want to test the external schema is put in correctly.

.. jsonschema:: subdir/test-without-compontent.json
   :allowexternalrefs:





Test without components - do NOT allow external refs!

We just want to make sure it does not crash, and the output is as sensible as possible.

.. jsonschema:: subdir/test-without-compontent.json



