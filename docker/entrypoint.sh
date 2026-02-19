#!/bin/bash
set -e

CONFIG_PATH="$1"

if [ -z "$CONFIG_PATH" ]; then
  echo "Usage: docker run image <config_file_path>"
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
