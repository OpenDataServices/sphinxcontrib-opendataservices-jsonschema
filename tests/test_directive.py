import re

import lxml.html
import pytest

from tests import path


def normalize(string):
    return re.sub(r'\n *', '', string)


def assert_build(app, status, warning, basename, buildername='html', messages=None):
    app.build()
    warnings = warning.getvalue().strip()

    if buildername == 'html':
        with open(path(basename, '_build', buildername, 'index.html'), encoding='utf-8') as f:
            element = lxml.html.fromstring(f.read()).xpath('//div[@class="documentwrapper"]')[0]
            actual = lxml.html.tostring(element).decode()

        with open(path(f'{basename}.html'), encoding='utf-8') as f:
            expected = f.read()

        assert normalize(actual) == normalize(expected)
    elif buildername == 'gettext':
        with open(path(basename, '_build', buildername, 'index.pot'), encoding='utf-8') as f:
            actual = re.sub(r"POT-Creation-Date: [0-9: +-]+", "POT-Creation-Date: ", f.read())

        with open(path(f'{basename}.pot'), encoding='utf-8') as f:
            expected = f.read()

        assert actual == expected

    assert 'build succeeded' in status.getvalue()

    if messages:
        for message in messages:
            assert message in warnings
        assert len(messages) == len(warnings.split('\n'))
    else:
        assert warnings == ''


@pytest.mark.sphinx(buildername='html', srcdir=path('basic'), freshenv=True)
def test_basic(app, status, warning):
    assert_build(app, status, warning, 'basic')


@pytest.mark.sphinx(buildername='gettext', srcdir=path('basic'), freshenv=True)
def test_basic_gettext(app, status, warning):
    assert_build(app, status, warning, 'basic', buildername='gettext')


@pytest.mark.sphinx(buildername='html', srcdir=path('basic-externallinks'), freshenv=True)
def test_basic_externallinks(app, status, warning):
    assert_build(app, status, warning, 'basic-externallinks')


@pytest.mark.sphinx(buildername='gettext', srcdir=path('basic-md'), freshenv=True)
def test_basic_gettext_myst(app, status, warning):
    assert_build(app, status, warning, 'basic-md', buildername='gettext')
