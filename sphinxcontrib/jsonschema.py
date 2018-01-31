"""

    sphinxcontrib.jsonschema
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by Takeshi KOMIYA <i.tkomiya@gmail.com>
    :license: BSD, see LICENSE for details.
"""
import io
import os
import sys
import jsonref
from jsonpointer import resolve_pointer
from six import string_types
from docutils import nodes
from docutils.statemachine import ViewList
from docutils.parsers.rst import directives, Directive
from docutils.utils import new_document
from recommonmark.parser import CommonMarkParser

if sys.version_info < (2, 7):
    import simplejson as json
    from ordereddict import OrderedDict
else:
    import json
    from collections import OrderedDict


class CustomJsonrefLoader(jsonref.JsonLoader):
    def get_remote_json(self, uri, **kwargs):
        return {}


class JSONSchemaDirective(Directive):
    has_content = True
    required_arguments = 1
    option_spec = {
        'include': directives.unchanged,
        'collapse': directives.unchanged,
        'pointer': directives.unchanged,
        'nocrossref': directives.flag,
    }
    # Add a rollup option here

    headers = ['Title', 'Description', 'Type', 'Format', 'Required']
    widths = [1, 1, 1, 1, 1]
    include = []
    collapse = []
    collapse_used = set()

    def run(self):
        include = self.options.get('include')
        if include:
            self.include = include.split(',')
        collapse = self.options.get('collapse')
        if collapse:
            self.collapse = collapse.split(',')

        env = self.state.document.settings.env
        try:
            if self.arguments and self.content:
                raise self.warning('both argument and content. it is invalid')
            if self.arguments:
                dirname = os.path.dirname(env.doc2path(env.docname, base=None))
                relpath = os.path.join(dirname, self.arguments[0])
                abspath = os.path.join(env.srcdir, relpath)
                if not os.access(abspath, os.R_OK):
                    raise self.warning('JSON Schema file not readable: %s' %
                                       self.arguments[0])
                env.note_dependency(relpath)

                schema = JSONSchema.loadfromfile(abspath)
            else:
                schema = JSONSchema.loadfromfile(''.join(self.content))
        except ValueError as exc:
            raise self.error('Failed to parse JSON Schema: %s' % exc)

        if self.options.get('pointer'):
            schema = JSONSchema.instantiate(None, resolve_pointer(schema.attributes, self.options.get('pointer')))

        return self.make_nodes(schema)

    def make_nodes(self, schema):
        table = self.table(schema)
        collapse_unused = set(self.collapse) - self.collapse_used
        if collapse_unused:
            msg = 'Collapse values don\'t exist: {}'.format(collapse_unused)
            return [self.state.document.reporter.warning(msg), table]
        else:
            return [table]

    def table(self, schema):
        tgroup = nodes.tgroup(cols=len(self.headers))
        for width in self.widths:
            tgroup += nodes.colspec(colwidth=width)

        table = nodes.table('', tgroup)
        header_row = nodes.row()
        for header in self.headers:
            header_row += self.cell(header, source='sphinxcontrib-jsonschema')

        tgroup += nodes.thead('', header_row)
        tbody = nodes.tbody()
        tgroup += tbody
        for prop in schema:
            if self.include and not prop.name.startswith(tuple(self.include)):
                continue
            if prop.name.startswith(tuple(self.collapse)):
                if prop.name in self.collapse:
                    self.collapse_used.add(prop.name)
                else:
                    continue
            if '^' in prop.name:
                # Skip patternProperties
                # Do this here to increase chances of upstreaming code changes
                # outside of the directive
                continue
            self.row(prop, tbody)

        return table

    def row(self, prop, tbody):
        row = nodes.row()
        anchor = '{},{},{}'.format(
            self.arguments[0].split('/')[-1],
            self.options.get('pointer', ''),
            prop.name)
        cell = nodes.entry('', nodes.target(ids=[anchor], names=[anchor]), nodes.literal('', nodes.Text(prop.name)),
                           morecols=1)
        row += cell
        row += self.cell(prop.type)
        row += self.cell(prop.format or '')
        row += self.cell('Required' if prop.required else '')
        tbody += row
        row = nodes.row()
        row += self.cell(prop.title)
        if prop.description:
            cell = self.cell(prop.description or '', morecols=3)
            if 'nocrossref' not in self.options:
                ref = None
                if hasattr(prop.attributes, '__reference__'):
                    ref = prop.attributes.__reference__['$ref']
                elif hasattr(prop.items, '__reference__'):
                    ref = prop.items.__reference__['$ref']
                if ref:
                    # just use the name at the end of the ref
                    ref = ref.split('/')[-1]
                    reference = nodes.reference('', '', nodes.Text(ref), internal=False, refuri='#' + ref.lower(),
                                                anchorname='')
                    cell += nodes.paragraph('', nodes.Text('\n\nSee '), reference)
                if prop.deprecated:
                    cell += nodes.paragraph('', nodes.Text('This property was deprecated in version {}'
                                                           .format(prop.deprecated['deprecatedVersion'])))
                    cell += nodes.paragraph('', nodes.Text(prop.deprecated['description']))
            row += cell
        tbody += row

    def cell(self, text, morecols=0, source=None):
        entry = nodes.entry(morecols=morecols)
        if not isinstance(text, string_types):
            text = str(text)

        parser = CommonMarkParser()
        new_doc = new_document(None)
        parser.parse(text, new_doc)

        viewlist = ViewList([child.astext() for child in new_doc.children[:]], source=source)
        self.state.nested_parse(viewlist, 0, entry)
        return entry


def get_class_for(obj):
    mapping = {
        'null': Null,
        'boolean': Boolean,
        'integer': Integer,
        'number': Number,
        'string': String,
        'array': Array,
        'object': Object,
    }
    if isinstance(obj, string_types):
        type = obj
    else:
        type = obj.get('type')
    if isinstance(type, list):
        # returns Union class for "type: [integer, number]"
        return Union(type)
    else:
        return mapping.get(type, Object)


def simplify(obj):
    if isinstance(obj, dict) and obj.keys() == ['type']:
        type = obj.get('type')
        if type is None:
            return 'null'
        elif isinstance(type, string_types):
            return json.dumps(type)
        else:
            return str(type)
    else:
        return json.dumps(obj)


class JSONSchema(object):
    @classmethod
    def load(cls, reader):
        obj = jsonref.load(reader, object_pairs_hook=OrderedDict, loader=CustomJsonrefLoader())
        return cls.instantiate(None, obj)

    @classmethod
    def loads(cls, string):
        obj = jsonref.loads(string, object_pairs_hook=OrderedDict, loader=CustomJsonrefLoader())
        return cls.instantiate(None, obj)

    @classmethod
    def loadfromfile(cls, filename):
        with io.open(filename, 'rt', encoding='utf-8') as reader:
            return cls.load(reader)

    @classmethod
    def instantiate(cls, name, obj, required=False, parent=None, rollup=True):
        return get_class_for(obj)(name, obj, required, parent, rollup)


def Union(types):
    class Union(JSONData):
        def __init__(self, name, attributes, required=False, parent=None, rollup=True):
            super(Union, self).__init__(name, attributes, required, parent, rollup)
            self.elements = []
            for type in types:
                elem = get_class_for(type)(name, attributes, required)
                self.elements.append(elem)

        @property
        def type(self):
            return '[%s]' % ', '.join(types)

        @property
        def validations(self):
            rules = []
            for elem in self.elements:
                rules.extend(elem.validations)

            return rules

    return Union


class JSONData(object):
    def __init__(self, name, attributes, required=False, parent=None, rollup=True):
        self.name = name or ''
        self.attributes = attributes
        self.required = required
        self.parent = parent
        self.rollup = rollup

    def __getattr__(self, name):
        if isinstance(self.attributes, dict):
            if hasattr(self.attributes, '__reference__'):
                if name in self.attributes.__reference__:
                    return self.attributes.__reference__[name]
            return self.attributes.get(name)
        else:
            return None

    def __iter__(self):
        return iter([])

    def get_typename(self):
        return self.type

    def stringify(self):
        return json.dumps(self.attributes)

    @property
    def validations(self):
        rules = []
        if 'enum' in self.attributes:
            enums = []
            for enum_type in self.enum:
                enums.append(simplify(enum_type))
            rules.append('It must be equal to one of the elements in [%s]' % ', '.join(enums))
        if 'allOf' in self.attributes:
            pass
        if 'anyOf' in self.attributes:
            pass
        if 'oneOf' in self.attributes:
            pass
        if 'not' in self.attributes:
            pass
        if 'definitions' in self.attributes:
            pass
        return rules

    @property
    def full_title(self):
        # Check for self.parent.name here so we don't get a title for the root
        # element
        if self.parent and self.parent.name:
            if self.parent.full_title and self.title:
                return self.parent.full_title + ':' + self.title
            else:
                return None
        else:
            return self.title


class Null(JSONData):
    type = "null"


class Boolean(JSONData):
    type = 'boolean'


class Integer(JSONData):
    type = 'integer'

    @property
    def validations(self):
        rules = super(Integer, self).validations
        if 'multipleOf' in self.attributes:
            rules.append('It must be multiple of %s' % self.multipleOf)
        if 'maximum' in self.attributes:
            if self.exclusiveMaximum:
                rules.append('It must be lower than %s' % self.maximum)
            else:
                rules.append('It must be lower than or equal to %s' % self.maximum)
        if 'minimum' in self.attributes:
            if self.exclusiveMinimum:
                rules.append('It must be greater than %s' % self.minimum)
            else:
                rules.append('It must be greater than or equal to %s' % self.minimum)
        return rules


class Number(Integer):
    type = 'number'


class String(JSONData):
    type = "string"

    @property
    def validations(self):
        rules = super(String, self).validations
        if 'maxLength' in self.attributes:
            rules.append('Its length must be less than or equal to %s' % self.maxLength)
        if 'minLength' in self.attributes:
            rules.append('Its length must be greater than or equal to %s' % self.minLength)
        if 'pattern' in self.attributes:
            rules.append('It must match to regexp "%s"' % self.pattern)
        if 'format' in self.attributes:
            rules.append('It must be formatted as %s' % self.format)
        return rules


class Array(JSONData):
    type = "array"

    @property
    def validations(self):
        rules = super(Array, self).validations
        if self.additionalItems is True:
            rules.append('It allows additional items')
        if 'maxItems' in self.attributes:
            rules.append('Its size must be less than or equal to %s' % self.maxItems)
        if 'minItems' in self.attributes:
            rules.append('Its size must be greater than or equal to %s' % self.minItems)
        if 'uniqueItems' in self.attributes:
            if self.uniqueItems:
                rules.append('Its elements must be unique')
        if isinstance(self.items, dict):
            item = JSONSchema.instantiate(self.name, self.items, parent=self)
            if item.type not in ('array', 'object'):
                rules.extend(item.validations)

        return rules

    def __iter__(self):
        if isinstance(self.items, dict):
            item = JSONSchema.instantiate(self.name + '/0', self.items, parent=self)

            # array object itself
            array = JSONSchema.instantiate(self.name, self.attributes, parent=self.parent)
            array.type = 'array[%s]' % item.get_typename()
            yield array

            # properties of items
            for prop in item:
                yield prop
        else:
            # create items and additionalItems objects
            items = []
            types = []
            for i, item in enumerate(self.items):
                name = '%s[%d]' % (self.name or '', i)
                items.append(JSONSchema.instantiate(name, item, parent=self))
                types.append(items[-1].get_typename())

            if isinstance(self.additionalItems, dict):
                name = '%s[%d+]' % (self.name or '', len(items))
                additional = JSONSchema.instantiate(name, self.additionalItems, parent=self)
                types.append(additional.get_typename() + '+')
            else:
                additional = None

            # array object itself
            array = JSONSchema.instantiate(self.name, self.attributes, parent=self)
            array.type = 'array[%s]' % ','.join(types)
            yield array

            # properties of items
            for item in items:
                yield item
                for prop in item:
                    yield prop

            # additionalItems
            if additional:
                yield additional

                for prop in additional:
                    yield prop


class Object(JSONData):
    type = "object"

    def get_typename(self):
        if self.title:
            return self.title
        else:
            return self.type

    @property
    def validations(self):
        rules = super(Object, self).validations
        if 'maxProperties' in self.attributes:
            rules.append('Its numbers of properties must be less than or equal to %s' % self.maxProperties)
        if 'minProperties' in self.attributes:
            rules.append('Its numbers of properties must be greater than or equal to %s' % self.minProperties)
        if 'required' in self.attributes:
            rules.append('Its property set must contains all elements in %s' % self.required)
        if 'dependencies' in self.attributes:
            for name, attr in self.dependencies.items():
                if isinstance(attr, dict):
                    rules.append('The "%s" property must match to %s' % (name, simplify(attr)))
                else:
                    attr = (simplify(name) for name in attr)
                    rules.append('The "%s" property depends on [%s]' % (name, ', '.join(attr)))
        return rules

    def __iter__(self):
        for prop in self.get_properties():
            if prop.type != 'array':
                yield prop

            if prop.type in ["object", "array"]:
                for subprop in prop:
                    yield subprop

    def get_properties(self):
        if self.name:
            prefix = self.name + '/'
        else:
            prefix = ''
        required = self.attributes.get('required', [])

        for name, attr in self.attributes.get('properties', {}).items():
            if isinstance(self.parent, Array):
                rollup = name in self.parent.attributes.get('rollUp', [])
            else:
                rollup = True
            yield JSONSchema.instantiate(prefix + name, attr, name in required, parent=self, rollup=rollup)

        for name, attr in self.attributes.get('patternProperties', {}).items():
            yield JSONSchema.instantiate(prefix + name, attr, parent=self)

        if isinstance(self.additionalProperties, dict):
            yield JSONSchema.instantiate(prefix + '*', attr, parent=self)

    @property
    def full_title(self):
        if isinstance(self.parent, Array):
            return self.parent.full_title
        else:
            return super().full_title()


def setup(app):
    app.add_directive('jsonschema', JSONSchemaDirective)
