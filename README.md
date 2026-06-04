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
- [Setup and Installation](#setup-and-installation)
  - [Common Steps](#common-steps)
  - [Option A: Local Installation](#option-a-local-installation)
  - [Option B: Docker](#option-b-docker)
- [Execution](#execution)
  - [Configure the render](#configure-the-render)
  - [Execute Obscura](#execute-obscura)
  - [Verify the output](#verify-the-output)
  - [Run testing framework and create coverage report](#run-testing-framework-and-create-coverage-report)
  - [Create documentation](#create-documentation)
- [Dependency Management](#dependency-management)
- [Contributing](#contributing)
- [License](#license)

## Setup and Installation

There are two ways to set up Obscura, depending on whether you want to run everything natively on your machine or inside a Docker container. Both options share a few common steps (cloning the repo and preparing the input/config folders); after that, follow the instructions for the option you want.

- **Option A: Local installation** – install Python dependencies via conda and use a local Blender install.
- **Option B: Docker** – run Obscura inside a self-contained container, without needing a local Blender install.

### Common Steps

**Prerequisites:**
- Install [Git](https://git-scm.com/install/)

**Steps:**

1. Clone the repository in your desired folder. This folder will be called folder `X` from now on.
```
git clone https://github.com/davidrudlstorfer/obscura.git
```

2. Prepare input files and configuration:
```
mkdir ./render/input
cp -r ./obscura/src/obscura/configs ./render/configs
```

- Once both steps are done, continue with [Option A](#option-a-local-installation) or [Option B](#option-b-docker) below.

### Option A: Local Installation

**Additional prerequisites:**
- Install Anaconda/Miniconda (recommended for environment management). Other ways to install Obscura are possible but here the installation procedure is explained based on a conda install.

**Steps:**

1. Create a new Anaconda environment based on the [`environment.yml`](./environment.yml) file:
```
conda env create -f environment.yml
```

2. Activate your newly created environment:
```
conda activate obscura
```

3. Initialize all submodules:
```
git submodule update --init --recursive
```

4. Install all necessary third party libraries for all submodules:
```
git submodule --quiet foreach --recursive pip install -e .
```

5. Install all Obscura requirements (latest versions):
```
pip install -e .
```
or install the pinned versions with:
```
pip install -e ."[safe]"
```

- Now you are up and running 🎉 Continue with [Execution](#execution).

### Option B: Docker

**Additional prerequisites:**
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) (must be running for the steps below)

There are two ways to get the Docker image:

- **Pull the pre-built image (coming soon):** once [#3](https://github.com/davidrudlstorfer/obscura/issues/3) is resolved.
- **Build the image yourself:** follow the steps below.

**Steps to build the Docker image yourself:**

1. Open the `entrypoint.sh` file and make sure the line endings are set to LF and not CRLF (in VSCode, bottom right of editor). Save the file.

2. Build the Docker image:
```
docker build --no-cache -f docker/Dockerfile -t blender-render-image .
```

- Now you are up and running 🎉 Continue with [Execution](#execution).

## Execution

The following steps apply regardless of which installation option you chose above.

### Configure the render

- Configure the `params.yaml` file located in `X/render/configs` as desired (where `X` is the folder you cloned the repository into).
- Update the input and output filepaths in the `params.yaml` file:
```
  input_file_path: "/workspace/runtime/input/sample.stl"
  output_file_path: "/workspace/runtime/output/render_sample.png"
```
- Change `sample.stl` and `render_sample.png` to match your own setup.

### Execute Obscura

- **If you installed locally (Option A):** run Obscura directly via the `obscura` console script (installed by `pip install -e .`):
```
obscura --config_file_path=./render/configs/params.yaml
```
Adjust the path to `params.yaml` if your folder `X` is located elsewhere.
- **If you installed via Docker (Option B):** run the container on a mounted volume:
```
docker run --rm -v "<PROJECT_PATH>\render:/workspace/runtime" blender-render-image --config_file_path=/workspace/runtime/configs/params.yaml
```
Replace `<PROJECT_PATH>` with the path to your local repository, folder `X`.

### Verify the output

- Check that rendering was successful by confirming an output file exists at `X/render/output/render_sample.png`.

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

Finally, performance critical packages such as Numpy and Numba are installed via conda to utilize BLAS libraries.

## Contributing

All contributions are welcome. See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for more information.

## License

This project is licensed under a MIT license. For further information check [`LICENSE.md`](./LICENSE.md).
