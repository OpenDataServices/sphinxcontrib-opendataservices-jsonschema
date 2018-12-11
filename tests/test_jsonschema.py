# -*- coding: utf-8 -*-

import sys
import json
from shutil import rmtree
from tempfile import mkdtemp, NamedTemporaryFile
from sphinxcontrib.jsonschema import JSONSchema

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestJsonSchema(unittest.TestCase):
    def test_instantiate(self):
        try:
            tmpdir = mkdtemp()
            tmpfile = NamedTemporaryFile('w+t', dir=tmpdir)

            data = {'type': 'string'}
            tmpfile.write(json.dumps(data))
            tmpfile.seek(0)

            # load from string
            schema = JSONSchema.loads(json.dumps(data))
            self.assertEqual(data, schema.attributes)

            # load from readable object
            schema = JSONSchema.load(tmpfile)
            self.assertEqual(data, schema.attributes)

            # load from file
            schema = JSONSchema.loadfromfile(tmpfile.name)
            self.assertEqual(data, schema.attributes)
        finally:
            tmpfile.close()
            rmtree(tmpdir)

    def test_attributes(self):
        data = """{
            "description": "test data",
            "title": "test-data-2001",
            "type": "number",
            "multipleOf": 20,
            "maximum": 100,
            "exclusiveMaximum": true,
            "default": 50,
            "example": null,
            "user_defined_attr_255": "255"
        }"""
        schema = JSONSchema.loads(data)
        self.assertEqual(schema.name, '')
        self.assertEqual(schema.description, 'test data')
        self.assertEqual(schema.title, 'test-data-2001')
        self.assertEqual(schema.type, 'number')
        self.assertEqual(schema.multipleOf, 20)
        self.assertEqual(schema.maximum, 100)
        self.assertEqual(schema.exclusiveMaximum, True)
        self.assertEqual(schema.default, 50)
        self.assertEqual(schema.example, None)
        self.assertEqual(schema.user_defined_attr_255, "255")

    def test_number_validations1(self):
        data = """{
            "type": "number",
            "multipleOf": 20,
            "maximum": 100,
            "minimum": 0
        }"""
        schema = JSONSchema.loads(data)
        self.assertEqual(schema.validations,
                         ['It must be multiple of 20',
                          'It must be lower than or equal to 100',
                          'It must be greater than or equal to 0'])

    def test_number_validations2(self):
        data = """{
            "type": "number",
            "maximum": 100,
            "exclusiveMaximum": false,
            "minimum": 0,
            "exclusiveMinimum": false
        }"""
        schema = JSONSchema.loads(data)
        self.assertEqual(schema.validations,
                         ['It must be lower than or equal to 100',
                          'It must be greater than or equal to 0'])

    def test_number_validations3(self):
        data = """{
            "type": "number",
            "maximum": 100,
            "exclusiveMaximum": true,
            "minimum": 0,
            "exclusiveMinimum": true
        }"""
        schema = JSONSchema.loads(data)
        self.assertEqual(schema.validations,
                         ['It must be lower than 100',
                          'It must be greater than 0'])

    def test_string_validations(self):
        data = """{
            "type": "string",
            "maxLength": 100,
            "minLength": 0,
            "pattern": "sources/.*\\\\.rst"
        }"""
        schema = JSONSchema.loads(data)
        self.assertEqual(schema.validations,
                         ['Its length must be less than or equal to 100',
                          'Its length must be greater than or equal to 0',
                          'It must match to regexp "sources/.*\\.rst"'])

    def test_array_validations1(self):
        data = """{
            "type": "array",
            "items": { "type": "number" },
            "maxItems": 100,
            "minItems": 0,
            "uniqueItems": true
        }"""
        schema = JSONSchema.loads(data)
        self.assertEqual(schema.validations,
                         ['Its size must be less than or equal to 100',
                          'Its size must be greater than or equal to 0',
                          'Its elements must be unique'])

    def test_array_validations2(self):
        data = """{
            "type": "array",
            "items": [
                { "type": "number" }
            ],
            "additionalItems": true
        }"""
        schema = JSONSchema.loads(data)
        self.assertEqual(schema.validations,
                         ['It allows additional items'])

    def test_array_validations3(self):
        data = """{
            "type": "array",
            "items": [
                { "type": "number" }
            ],
            "additionalItems": false
        }"""
        schema = JSONSchema.loads(data)
        self.assertEqual(schema.validations, [])

    def test_array_validations4(self):
        data = """{
            "type": "array",
            "items": {
                    "type": "number",
                    "maximum": 100
            },
            "additionalItems": false
        }"""
        schema = JSONSchema.loads(data)
        self.assertEqual(schema.validations,
                         ['It must be lower than or equal to 100'])

    def test_object_validations1(self):
        data = """{
            "type": "object",
            "maxProperties": 5,
            "minProperties": 2,
            "dependencies": {
                "subclass": ["class"],
                "total_price": ["price", "tax"]
            }
        }"""
        schema = JSONSchema.loads(data)
        self.assertEqual(schema.validations,
                         ['Its numbers of properties must be less than or equal to 5',
                          'Its numbers of properties must be greater than or equal to 2',
                          'The "subclass" property depends on ["class"]',
                          'The "total_price" property depends on ["price", "tax"]'])

    def test_object_validations2(self):
        data = """{
            "type": "object",
            "maxProperties": 5,
            "minProperties": 2,
            "dependencies": {
                "subclass": {
                    "type": "string",
                    "minLength": 5
                }
            }
        }"""
        schema = JSONSchema.loads(data)
        self.assertEqual(schema.validations,
                         ['Its numbers of properties must be less than or equal to 5',
                          'Its numbers of properties must be greater than or equal to 2',
                          'The "subclass" property must match to {"type": "string", "minLength": 5}'])

    def test_enum_validation(self):
        data = """{
            "type": "object",
            "enum": [
                "string",
                {
                    "type": "object",
                    "maxProperties": 3
                },
                null,
                42
            ]
        }"""
        schema = JSONSchema.loads(data)
        self.assertEqual(schema.validations,
                         ['It must be equal to one of the elements '
                          'in ["string", {"type": "object", "maxProperties": 3}, null, 42]'])

# Validation for any instance type

    def test_semantic_validations(self):
        data = """{
            "type": "string",
            "format": "email"
        }"""
        schema = JSONSchema.loads(data)
        self.assertEqual(schema.validations,
                         ['It must be formatted as email'])

    def test_list_object_properties1(self):
        data = """{
            "type": "array",
            "items": {
                "type": "number",
                "multipleOf": 1
            },
            "uniqueItems": false
        }"""
        schema = JSONSchema.loads(data)
        props = list(schema)
        self.assertEqual(len(props), 1)

        self.assertEqual(props[0].name, '')
        self.assertEqual(props[0].type, 'array[number]')

    def test_list_object_properties2(self):
        data = """{
            "type": "array",
            "items": {
                "type": "object",
                "title": "Human"
            },
            "uniqueItems": false
        }"""
        schema = JSONSchema.loads(data)
        props = list(schema)
        self.assertEqual(len(props), 1)

        self.assertEqual(props[0].name, '')
        self.assertEqual(props[0].type, 'array[Human]')

    def test_list_object_properties3(self):
        data = """{
            "type": "array",
            "items": [
                { "type": "number" },
                { "type": "string" },
                { "type": "number" }
            ]
        }"""
        schema = JSONSchema.loads(data)
        props = list(schema)
        self.assertEqual(len(props), 4)

        self.assertEqual(props[0].name, '')
        self.assertEqual(props[0].type, 'array[number,string,number]')

        self.assertEqual(props[1].name, '[0]')
        self.assertEqual(props[1].type, 'number')

        self.assertEqual(props[2].name, '[1]')
        self.assertEqual(props[2].type, 'string')

        self.assertEqual(props[3].name, '[2]')
        self.assertEqual(props[3].type, 'number')

    def test_list_object_properties4(self):
        data = """{
            "type": "array",
            "items": [
                { "type": "number" },
                { "type": "string" },
                { "type": "number" }
            ],
            "additionalItems": {
                "type": "object",
                "properties": {
                    "name": "string"
                }
            }
        }"""
        schema = JSONSchema.loads(data)
        props = list(schema)
        self.assertEqual(len(props), 6)

        self.assertEqual(props[0].name, '')
        self.assertEqual(props[0].type, 'array[number,string,number,object+]')

        self.assertEqual(props[1].name, '[0]')
        self.assertEqual(props[1].type, 'number')

        self.assertEqual(props[2].name, '[1]')
        self.assertEqual(props[2].type, 'string')

        self.assertEqual(props[3].name, '[2]')
        self.assertEqual(props[3].type, 'number')

        self.assertEqual(props[4].name, '[3+]')
        self.assertEqual(props[4].type, 'object')

        self.assertEqual(props[5].name, '[3+]/name')
        self.assertEqual(props[5].type, 'string')

    def test_list_object_properties5(self):
        data = """{
            "type": "object",
            "properties": {
                "name": "string",
                "password": "string",
                "address" : {
                    "type": "object",
                    "properties": {
                        "prefecture": "string",
                        "postal_code": "string"
                    }
                }
            },
            "required": ["name"]
        }"""
        schema = JSONSchema.loads(data)
        props = list(schema)
        self.assertEqual(len(props), 5)

        self.assertEqual(props[0].name, 'name')
        self.assertEqual(props[0].type, 'string')
        self.assertEqual(props[0].required, True)

        self.assertEqual(props[1].name, 'password')
        self.assertEqual(props[1].type, 'string')
        self.assertEqual(props[1].required, False)

        self.assertEqual(props[2].name, 'address')
        self.assertEqual(props[2].type, 'object')
        self.assertEqual(props[2].required, False)

        self.assertEqual(props[3].name, 'address/prefecture')
        self.assertEqual(props[3].type, 'string')
        self.assertEqual(props[3].required, False)

        self.assertEqual(props[4].name, 'address/postal_code')
        self.assertEqual(props[4].type, 'string')
        self.assertEqual(props[4].required, False)

    def test_list_object_properties6(self):
        "An object containing an array of objects."

        data = """{
            "type": "object",
            "properties": {
                "addresses": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "prefecture": "string"
                        }
                    }
                }
            }
        }"""
        schema = JSONSchema.loads(data)
        props = list(schema)
        self.assertEqual(len(props), 2)

        self.assertEqual(props[0].name, 'addresses')
        self.assertEqual(props[0].type, 'array[object]')
        self.assertEqual(props[0].required, False)

        self.assertEqual(props[1].name, 'addresses/0/prefecture')
        self.assertEqual(props[1].type, 'string')
        self.assertEqual(props[1].required, False)

    def test_list_object_properties6b(self):
        """
        Same as test_list_object_properties6, except type is array or null.

        """
        data = """{
            "type": "object",
            "properties": {
                "addresses": {
                    "type": ["array", "null"],
                    "items": {
                        "type": "object",
                        "properties": {
                            "prefecture": "string"
                        }
                    }
                }
            }
        }"""
        schema = JSONSchema.loads(data)
        props = list(schema)
        self.assertEqual(len(props), 2)

        self.assertEqual(props[0].name, 'addresses')
        self.assertEqual(props[0].type, 'array[object]')
        self.assertEqual(props[0].required, False)

        self.assertEqual(props[1].name, 'addresses/0/prefecture')
        self.assertEqual(props[1].type, 'string')
        self.assertEqual(props[1].required, False)

    def test_list_object_properties7(self):
        "An object containing an array of strings."

        data = """{
            "type": "object",
            "properties": {
                "addresses": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        }"""
        schema = JSONSchema.loads(data)
        props = list(schema)
        self.assertEqual(len(props), 1)

        self.assertEqual(props[0].name, 'addresses')
        self.assertEqual(props[0].type, 'array[string]')
        self.assertEqual(props[0].required, False)

    def test_list_object_properties7b(self):
        """
        Same as test_list_object_properties7, except type is array or null.

        """
        data = """{
            "type": "object",
            "properties": {
                "addresses": {
                    "type": ["array", "null"],
                    "items": {
                        "type": "string"
                    }
                }
            }
        }"""
        schema = JSONSchema.loads(data)
        props = list(schema)
        self.assertEqual(len(props), 1)

        self.assertEqual(props[0].name, 'addresses')
        self.assertEqual(props[0].type, 'array[string]')
        self.assertEqual(props[0].required, False)

    def test_union_validations(self):
        data = """{
            "type": ["number", "string"],
            "title": "union title",
            "description": "union description",
            "maximum": 100,
            "minimum": 0,
            "maxLength": 100,
            "minLength": 0
        }"""
        schema = JSONSchema.loads(data)
        self.assertEqual(schema.description, 'union description')
        self.assertEqual(schema.title, 'union title')
        self.assertEqual(schema.type, '[number, string]')
        self.assertEqual(schema.maximum, 100)
        self.assertEqual(schema.minimum, 0)
        self.assertEqual(schema.maxLength, 100)
        self.assertEqual(schema.minLength, 0)
        self.assertEqual(schema.validations,
                         ['It must be lower than or equal to 100',
                          'It must be greater than or equal to 0',
                          'Its length must be less than or equal to 100',
                          'Its length must be greater than or equal to 0'])
