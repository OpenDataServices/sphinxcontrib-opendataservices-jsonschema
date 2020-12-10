Developers
==========

The documentation for this widget directly includes use of this extension in the example pages!

To build these locally, create a new virtual environment then run:

.. code:: bash

    pip install -r requirements_dev.txt
    python -m sphinx docs/ docs/_out/

As well as providing documentation for others (always good!) this also provides a nice development environment for when
you are working on bugs or new features. Set up an example that should show your work; build the docs; see if your code
worked!

To make these docs build on Read The Docs, you need to:

* Set `requirements_dev.txt` as a `Requirements file`
* Disable `Enable PDF build`
* Disable `Enable EPUB build`
