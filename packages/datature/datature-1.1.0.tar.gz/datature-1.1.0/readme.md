# Datatue Python SDK

## Get started

- [Documentation](#documentation)
- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [Unit Test](#unit-test)

## Documentation

See the [API docs](https://developers.datature.io/).

## Installation

```sh
pip install --upgrade datature
```

### Requirements

- Python 3.7+

## Usage

The library needs to be configured with your project's secret key which is available in your Project Dashboard `Advanced/API Management`

```python
import datature
datature.secret_key = "6874c3c9b..."

# retrieve project
project = datature.Project.retrieve()

# print project information
print(project)

# retrieve project insight
insight = datature.Project.insight()

# print insight details
print(insight)

# list all assets
assets = datature.Asset.list()

# print the assets
print(assets)
```

## CLI

The CLI is part of `datature` package, once installed the package `datature` will be available from the command line.

### PATH

For those who may encounter a `datature not found` issue, please try setting the `PATH` manually:

```shell
export PATH="${PATH}:$(python3 -c 'import site; print(site.USER_BASE)')/bin"
```

### Functions

```shell
datature project auth

datature project select

datature project list

datature asset upload

datature asset group

datature annotation upload

datature annotation download

datature artifact download
```

## Unit Test

To run the tests, run command:

```sh
python -m coverage run -m unittest
```
