
project = 'sphinxcontrib-opendataservices-jsonschema'

master_doc = 'index'

extensions = ['sphinxcontrib.jsonschema', 'sphinx_rtd_theme']

html_extra_path = [
    'example_components.json',
    'example_schema.json',
    'example_schema_with_external_refs.json'
]

html_theme = "sphinx_rtd_theme"
