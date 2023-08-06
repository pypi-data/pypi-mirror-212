# Testing weeve_modules Package

Testing process for weeve_modules package should have two following stages:

* Test locally
* Test deployment to PyPI with [TestPyPI](https://test.pypi.org)

## Local testing

Local testing will simulate the weeve Edge Application with four modules (one input, two processing and one output). Details of the test Edge Application can be found in `docker-compose.test.yml`. After the Edge Application is set up, then sample data are sent through. Each tested module will save the incoming and outgoing data. Later the testing script (`test_package.py`) will compare that to the ground truth expected data. You must have Docker running for this test.

From the root directory, run local tests with the following command:

```bash
python3 -m pytest test/test_package.py -v
```

## TestPyPI

[TestPyPI](https://test.pypi.org) is a separate instance of the [Python Package Index (PyPI)](#https://packaging.python.org/en/latest/glossary/#term-Python-Package-Index-PyPI) that allows you to try out the distribution tools and process without worrying about affecting the real index. The package must be tested with TestPyPI before pushing to production.

Basically, the process requires registering your account on [TestPyPI](https://test.pypi.org) and pushing the package to the repository.

More details on using TestPyPI can be found [here](https://packaging.python.org/en/latest/guides/using-testpypi/).

Example of using TestPyPI can be found [here](https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives)



