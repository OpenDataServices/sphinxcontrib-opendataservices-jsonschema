# -*- coding: utf-8 -*-

from sphinx_testing import with_app

import unittest


class TestJsonSchema(unittest.TestCase):
    @with_app(srcdir='tests/examples/basic')
    def test_basic(self, app, status, warning):
        app.build()  # succeeded!
