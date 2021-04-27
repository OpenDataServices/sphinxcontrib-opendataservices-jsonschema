# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = open('README.rst').read()

setup(
    name='sphinxcontrib-opendataservices-jsonschema',
    version='0.1.0',
    url='https://github.com/OpenDataServices/sphinxcontrib-opendataservices-jsonschema',
    license='BSD',
    author='Takeshi KOMIYA & Open Data Services Co-operative',
    author_email='code@opendataservices.coop',
    description='Sphinx extension to define data structure using JSON Schema',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'docutils',
        'jsonref',
        'jsonpointer',
        'myst-parser',
    ],
    namespace_packages=['sphinxcontrib'],
)
