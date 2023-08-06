# MkDocs Iframe Plugin

[![ci](https://github.com/josham/mkdocs-iframe/workflows/ci/badge.svg)](https://github.com/josham/mkdocs-iframe/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://josham.github.io/mkdocs-iframe/)
[![pypi version](https://img.shields.io/pypi/v/mkdocs-iframe.svg)](https://pypi.org/project/mkdocs-iframe/)

MkDocs plugin to integrate HTML reports into your site.
This is a modified version of [mkdocs-coverage](https://github.com/pawamoy/mkdocs-coverage).

## Installation

With `pip`:
```bash
pip install mkdocs-iframe
```

With [`pipx`](https://github.com/pipxproject/pipx):
```bash
python -m pip install --user pipx
pipx install mkdocs-iframe
```

## Usage

You first need generate your html test reports. For example, using
[pytest-cov](https://github.com/pytest-dev/pytest-cov) and 
[pytest-html](https://github.com/pytest-dev/pytest-html):

```sh
pytest --cov --html=htmltest/index.html tests
coverage html
```

will generate two report directories `htmlcov` and `htmltest`.

Now update your `MkDocs` config:

```yaml
# mkdocs.yml

nav:
  - Coverage report: cov.md  # Needs to match page from below
  - Test report: test.md  # Needs to match page from below

plugins:
  - iframe:
      reports:
        - name: cov
          path: htmlcov  # default f"html{name}"
          root: index.html  # default
          page: cov.md  # f"{name}.md"
        - name: test
          path: htmltest  # default f"html{name}"
          root: index.html  # default
          page: test.md  # f"{name}.md"
```

Give the default settings, you could also use the following, simpler config:

```yaml
# mkdocs.yml

nav:
  - Coverage report: cov.md
  - Test report: test.md

plugins:
  - iframe:
      reports:
        - cov
        - test
```

Now serve your docs and go to http://localhost:8000/cov/ or http://localhost:8000/test/ to see your test report.

![coverage index](https://github.com/josham/mkdocs-iframe/assets/3686522/71576f61-7bc4-49c5-83d9-6c4234ef3686)
![test index](https://github.com/josham/mkdocs-iframe/assets/3686522/8e51b2f3-b48f-4220-982f-ee70a140d057)
