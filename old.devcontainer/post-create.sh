#!/usr/bin/env bash

source /opt/container/helpers/common/paths.sh
mkdir -p /config

# Required to get automations to work
echo "Creating automations.yaml"
touch /config/automations.yaml

# source: /opt/container/helpers/commons/homeassistant/start.sh
if test -d "custom_components"; then
  echo "Symlink the custom component directory"

  if test -d "custom_components"; then
    rm -R /config/custom_components
  fi

  ln -sf "$(workspacePath)custom_components/" /config/custom_components || echo "Could not copy the custom_component" exit 1
elif  test -f "__init__.py"; then
  echo "Having the component in the root is currently not supported"
fi

# Install
echo "Install home assistant"
container install

# Setup the Dev Stuff

pip install poetry
# We're in Docker, so we don't need a VENV
poetry config virtualenvs.create false
poetry install --no-interaction

# Keep this inline with any requirements that are in manifest.json
pip install git+https://github.com/zabuldon/teslajsonpy.git@dev#teslajsonpy==3.8.1
