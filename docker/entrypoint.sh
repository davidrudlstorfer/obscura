#!/bin/bash
set -e

# First argument is the config file path
CONFIG_PATH="$1"

# Check that a config file path was provided and correct
if [ -z "$CONFIG_PATH" ]; then
  echo "Error: a config file path must be provided."
  echo "Usage: docker run <image> <--config_file_path=[...]>"
  exit 1
fi

/opt/blender/blender \
  --background \
  --python-expr "
import obscura.main as cli
import sys
sys.argv = ['obscura', '$CONFIG_PATH']
cli.main()
"
