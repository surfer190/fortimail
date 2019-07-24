# Fortimail Rest API Client

This package is used to communicate with the fortimail rest api

## Install

    pip install fortimail

## Usage

    from fortimail.client import FortiMailClient
    
    client = FortiMailClient(
        baseurl='myfortimail.com',
        username='hello',
        password='world'
    )
    
    domains = client.get_domains()

## Developing

As per the [pytest best practices](https://docs.pytest.org/en/latest/goodpractices.html#test-discovery)

Create your environment

    python3.7 -m venv env
    pip install -r requirements/dev.txt
    # Install the package in editable mode
    pip install -e .

this is similar to running: `python setup.py develop`

## Run Tests

We use pytest, To run tests do: `pytest -s`

Soon to bring in tox - test automation - for different python versions

## Uploading to Pypi

    pip install wheel twine

Make sure to bump the version in `setup.py`

Create the `dist` and `build` folders

    python setup.py sdist bdist_wheel

Upload to test pypi

    twine upload --repository testpypi dist/*

Upload to real pypi

    twine upload --repository pypi dist/*