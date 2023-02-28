#!/bin/bash

PANDORA_ARGS=""

if [ -n "${PANDORA_PROXY}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} -p ${PANDORA_PROXY}"
fi

if [ -n "${PANDORA_ACCESS_TOKEN}" ]; then
  CONFIG_DIR="${HOME}/.config/Pandora-ChatGPT"
  mkdir -p "${CONFIG_DIR}"

  echo "${PANDORA_ACCESS_TOKEN}" >"${CONFIG_DIR}/access_token.dat"
fi

if [ -n "${PANDORA_SERVER}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} -s ${PANDORA_SERVER}"
fi

if [ -n "${PANDORA_VERBOSE}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} -v"
fi

# shellcheck disable=SC2086
$(command -v pandora) ${PANDORA_ARGS}
