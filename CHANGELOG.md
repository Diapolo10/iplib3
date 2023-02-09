
# IPlib3 Changelog

All notable changes to this project will be documented in this file.

The format is based on [CHANGELOG.md][CHANGELOG.md]
and this project adheres to [Semantic Versioning][Semantic Versioning].

<!-- 
TEMPLATE

## [major.minor.patch] - yyyy-mm-dd

A message that notes the main changes in the update.

### Added

### Changed

### Deprecated

### Fixed

### Removed

### Security

_______________________________________________________________________________
 
 -->

<!--
EXAMPLE

## [0.2.0] - 2021-06-02

Lorem Ipsum dolor sit amet.

### Added

- Cat pictures hidden in the library
- Added beeswax to the gears

### Changed

- Updated localisation files

-->

<!--
_______________________________________________________________________________

## [0.2.3] - 2023-02-09

Updated dependencies, stopped ignoring `poetry.lock`, and upgraded workflows.

### Added

- New workflows for code analysis and automatic dependency updates
- Automated GitHub releases

### Changed

- `poetry.lock` is now included in the repository
- Updated project metadata files for consistency
- Updated old workflows

### Removed

- The old `deploy.yml` was removed in favour of `pypi_deploy.yml`

-->

_______________________________________________________________________________

## [0.2.3] - 2023-02-09

Updated dependencies, stopped ignoring `poetry.lock`, and upgraded workflows.

### Added

- New workflows for code analysis and automatic dependency updates
- Automated GitHub releases

### Changed

- `poetry.lock` is now included in the repository
- Updated project metadata files for consistency
- Updated old workflows

### Removed

- The old `deploy.yml` was removed in favour of `pypi_deploy.yml`

_______________________________________________________________________________

## [0.2.2] - 2021-08-25

Small changes, such as the new `Makefile`.

### Added

- Added a `Makefile` to make testing the codebase easier/more streamlined locally on Linux/Unix platforms
- Added Tox as a development dependency

### Changed

- Changed the `README.md` badge chain to a table with the badges split into categories
- Updated localisation files

### Removed

- Removed `pytest-runner` as a development dependency, as it's useless with Poetry

_______________________________________________________________________________

## [0.2.1] - 2021-06-30

A quick fix to resolve Snyk throwing errors due to the empty `requirements.txt`
file.

### Changed

- Updated localisation files

### Fixed

- Snyk throwing a fit on pull requests
- Missing coverage from `iplib3.address`

### Removed

- `requirements.txt`

_______________________________________________________________________________

## [0.2.0] - 2021-06-29

This release focuses mostly on back-end changes, but there are a few additions
to functionality as well. Things have moved around, new unit tests have been
added, and the overall structure of the project is now more manageable. Most
importantly, however, the project has now been transitioned to use `poetry` as
its build system and this transition has enabled many of the old config files
to be removed. The entire project now uses `pyproject.toml` for all
configuration, from builds to unit tests. In addition, the GitHub Actions
workflow has been split into multiple workflows, it now uses Tox, and the
project is now additionally linted using `flake8`; previously only `pylint`
was used.

### Added

- `iplib3.constants`, a new sub-package used to store all of the constant
  values used by the project.
- `iplib3.subnet`, a new submodule housing new subnet objects. At this
  stage they remain unused, though the code has been unit tested.
- `iplib3.validators`, a new submodule for validator functions.

### Changed

- Validator functions from `iplib3.address` and `iplib3.subnet` have been
  moved to `iplib3.validators` to keep the codebase more maintainable.
- Constants originally defined in `iplib3.address` and `iplib3.subnet`
  have been moved to `iplib3.constants`.
- Some validators, including `port_validator`, `ip_validator`,
  `ipv4_validator`, `ipv6_validator`, and `subnet_validator`, have been
  added to the public interface. Previously they were considered private.
- Steps have been taken to reduce code duplication and complexity by creating
  new, currently private helper functions. This will be a key point in
  future development.
- `iplib3.PureAddress` is no longer an abstract base class, as it caused
  difficulties in unit testing. It has been reworked into a concrete class.
- Updated localisation files

### Deprecated

- The `requirements.txt`-file is no longer used for anything, it may be removed
  in a future version. Then again, it has been kept empty so far as the library
  currently lacks non-development dependencies.

### Fixed

- Hundreds of linter errors
- Unit test coverage (previously ~70%, now 100%)
- Bugs related to equality testing of addresses
- Bugs related to initialisation and construction of `iplib3.IPAddress`

### Removed

- `setup.cfg`
- `setup.py`
- Scripts related to running tests (now handled by Makefile and/or Poetry)

### Security

- Added Snyk integration to sniff out vulnerabilities

_______________________________________________________________________________

## [0.1.5] - 2021-05-01

This is the beginning of the changelog. Previously made commits have not been
tracked, and there are no plans to distinguish them. You may consider this
the initial commit.

### Added

- Added project URLs, more classifiers,
  and a minimum Python version requirement to PyPI

### Changed

- Unit tests are now also run on Windows and Mac OS during the CI/CD process
- The releases are now built on the latest version of Ubuntu, using Python 3.9
- The badges in README were split to separate lines to improve readability

### Fixed

- Fixed the CI/CD build process

[CHANGELOG.md]: https://web.archive.org/web/20220330064336/https://changelog.md/
[Semantic Versioning]: http://semver.org/

<!-- markdownlint-configure-file {
    "MD022": false,
    "MD024": false,
    "MD030": false,
    "MD032": false
} -->
<!--
    MD022: Blanks around headings
    MD024: No duplicate headings
    MD030: Spaces after list markers
    MD032: Blanks around lists
-->
