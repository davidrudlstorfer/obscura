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
  - [Generate configuration schema](#generate-configuration-schema)
  - [Run testing framework and create coverage report](#run-testing-framework-and-create-coverage-report)
  - [Create documentation](#create-documentation)
- [Dependency Management](#dependency-management)
- [Contributing](#contributing)
- [License](#license)

## Setup and Installation

There are multiple ways to set up Obscura, depending on whether you want to run everything natively on your machine or inside a Docker container. All options share a few common steps (cloning the repo and preparing the input/config folders); after that, follow the instructions for the option you want.

- **Option A: Local installation** – install Python dependencies via conda and use a local Blender install.
- **Option B: Docker** – run Obscura inside a self-contained container, without needing a local Blender install.

### Common Steps



1. Clone the repository
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
pip install -e ."[safe]"
```

- Now you are up and running 🎉

### Option B: Docker

**Additional prerequisites:**
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) (must be running for the steps below)

There are two ways to get the Docker image:

- **Build the image yourself:** follow the steps below.

**Steps to build the Docker image yourself:**


1. Build the Docker image:
```
docker build --no-cache -f docker/Dockerfile -t blender-render-image .
```

- Now you are up and running 🎉

## Execution

### Configure the render

- Configure the `params.yaml` file located in `/render/configs` as desired
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
- **If you installed via Docker (Option B):** run the container on a mounted volume:

Without a GPU, or to force CPU rendering:
```
 docker run --rm -v "<PROJECT_PATH>\render:/workspace/runtime" blender-render-image --config_file_path=/workspace/runtime/configs/params.yaml
 ```
 With an NVIDIA GPU:
```
 docker run --rm --gpus all -v "<PROJECT_PATH>\render:/workspace/runtime" blender-render-image --config_file_path=/workspace/runtime/configs/params.yaml
```
Replace `<PROJECT_PATH>` with the path to your local repository.

### Verify the output

- Check that rendering was successful by confirming an output file exists at `X/render/output/render_sample.png`.

### Generate configuration schema

The JSON schema for the configuration file can be generated using:

```bash
python src/obscura/generate_schema.py
```

This will create the `config_schema.json` file in the project root directory.

The generated schema can be used by VS Code to provide YAML validation and autocompletion for configuration files.

To enable schema validation in VS Code, add the following entry to your `settings.json`:

```json
{
    "yaml.schemas": {
        "./config_schema.json": "**/params.yaml"
    }
}
```

### Run testing framework and create coverage report

To locally execute the tests and create the html coverage report simply run

```bash
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
