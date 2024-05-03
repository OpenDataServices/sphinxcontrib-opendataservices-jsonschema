# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.7.0] - 2024-05-03

### Changed

- Add custom loader to resolve urn: references schema files

### Fixed

- Pin flake8<6 for linting
- Require lxml and defusedxml for tests
- myst-parser-version<0.18.0 removed from test matrix, as too old and massive dependency issues

## [0.6.1] - 2023-10-18

### Fixed

- Output row for an array even if items property is missing https://github.com/OpenDataServices/sphinxcontrib-opendataservices-jsonschema/issues/56

## [0.6.0] - 2023-08-31

### Changed

- Replace '_' with '-' in HTML anchors https://github.com/OpenDataServices/sphinxcontrib-opendataservices-jsonschema/pull/51
- Add myst-parser 0.19.0, 1 and 2 support (Changes API in myst-parser we use)
- Removed Python 3.7 and below support

## [0.5.1] - 2022-12-01

### Fixed

- Make work with all versions of jsonref

## [0.5.0] - 2022-07-20

### Fixed

- Set default `base_uri` correctly, fixes `jsonref.JsonRefError: Unresolvable JSON pointer`
- Arrays of string are now correctly marked as Required, if that's what the schema indicates

### Added

- Add myst-parser 0.18.0 support

## [0.4.0] - 2021-11-04

### Added

- Add `externallinks` option to `jsonschema` directive https://github.com/OpenDataServices/sphinxcontrib-opendataservices-jsonschema/issues/24
- Add `allowexternalrefs` option to `jsonschema` directive, off by default to preserve backwards compatibility
  https://github.com/OpenDataServices/sphinxcontrib-opendataservices-jsonschema/issues/24

## [0.3.0] - 2021-05-12

### Added

- Add `addtargets` option to `jsonschema` directive https://github.com/OpenDataServices/lib-cove-web/pull/96

## [0.2.0] - 2021-04-28

### Changed

- Removed Python 2 Support
- Remove use of `six` library (This was not included in `setup.py` anyway, which was a bug.)
- Switch to MyST-Parser from recommonmark https://github.com/OpenDataServices/sphinxcontrib-opendataservices-jsonschema/pull/27
- Correct the requirements https://github.com/OpenDataServices/sphinxcontrib-opendataservices-jsonschema/pull/28


## [0.1.0] - 2020-05-29

First release of new forked project
