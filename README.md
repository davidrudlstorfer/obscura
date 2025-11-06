<h1 align="center">
  🎥🐋 Obscura 🐋🎥
</h1>

<div align="center">

[![CI Workflow](https://github.com/davidrudlstorfer/obscura/actions/workflows/ci.yml/badge.svg)](https://github.com/davidrudlstorfer/obscura/actions/workflows/ci.yml)
[![Documentation](https://raw.githubusercontent.com/davidrudlstorfer/obscura/refs/heads/main/assets/badges/documentation.svg)](https://davidrudlstorfer.github.io/obscura/)
[![Coverage badge](https://github.com/davidrudlstorfer/obscura/raw/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/davidrudlstorfer/obscura/blob/python-coverage-comment-action-data/htmlcov/index.html)

</div>

Obscura is a self-contained Docker environment that simplifies rendering with Blender and Python, enabling automated, headless visualization workflows without manual setup.

The remaining parts of the readme are structured as follows:

- [Setup](#setup)
- [Installation](#installation)
- [Execution](#execution)
  - [Execute Obscura](#execute-obscura)
  - [Run testing framework and create coverage report](#run-testing-framework-and-create-coverage-report)
  - [Create documentation](#create-documentation)
- [Dependency Management](#dependency-management)
- [Contributing](#contributing)
- [License](#license)


## Setup

TBD

## Installation

For a quick and easy start an Anaconda/Miniconda environment is highly recommended. Other ways to install Obscura are possible but here the installation procedure is explained based on a conda install. After installing Anaconda/Miniconda
execute the following steps:

- Create a new Anaconda environment based on the [`environment.yml`](./environment.yml) file:
```
conda env create -f environment.yml
```

- Activate your newly created environment:
```
conda activate obscura
```

- Initialize all submodules
```
git submodule update --init --recursive
```

- All necessary third party libraries for all submodules can be installed using:
```
git submodule --quiet foreach --recursive pip install -e .
```

- Install all Obscura requirements (latest versions) with:
```
pip install -e .
```
or install the pinned versions with
```
pip install -e ."[safe]"
```

- Now you are up and running 🎉

## Execution

### Execute Obscura

TBD

### Run testing framework and create coverage report

To locally execute the tests and create the html coverage report simply run

```
pytest
```

### Create documentation

To locally create the documentation from the provided docstrings simply run

```
pdoc --docformat google --output-dir docs src/obscura
```

## Dependency Management

To ease the dependency update process [`pip-tools`](https://github.com/jazzband/pip-tools) is utilized. To create the necessary [`requirements.txt`](./requirements.txt) file simply execute

```
pip-compile --all-extras --output-file=requirements.txt requirements.in
```

To upgrade the dependencies simply execute

```
pip-compile --all-extras --output-file=requirements.txt --upgrade requirements.in
```

Finally, perforfmance critical packages such as Numpy and Numba are installed via conda to utilize BLAS libraries.

## Contributing

All contributions are welcome. See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for more information.

## License

This project is licensed under a MIT license. For further information check [`LICENSE.md`](./LICENSE.md).
