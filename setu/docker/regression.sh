#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
ROOT_DIR="$(dirname ${DIR})"
WORKSPACE_DIR="$(dirname ${ROOT_DIR})"
RESULT_DIR="/setu"

# Run with START_DEPENDENCIES_ONLY=true ./integration-tests.sh to only bring up
# the dependencies and allow for local development
START_DEPENDENCIES_ONLY=${START_DEPENDENCIES_ONLY:-false}

RUNNER_IMAGE=${RUNNER_IMAGE:-curlimages/curl:7.70.0}

set -ex

if [[ "${START_DEPENDENCIES_ONLY}" == "false" ]]; then
  # Build tests
  pushd "${WORKSPACE_DIR}"

  if [ -z ${CONTAINER_NAME} ]; then
    # If no container name in env then create one
    CONTAINER_NAME="setu-$(date +%s)"
  fi

  docker build --no-cache -t ${CONTAINER_NAME} ./ -f "${DIR}/regression.dockerfile"

  # Run integration tests
  docker run \
      -it -d --name "${CONTAINER_NAME}" \
      ${CONTAINER_NAME} /bin/bash

  set +e


  docker exec "${CONTAINER_NAME}" python -m pytest -s /setu/tests \
        -k "${TEST_SELECTOR}" \
        --alluredir="${RESULT_DIR}/allure-report" \
        --junitxml "${RESULT_DIR}/setu.xml" \
        --html "${RESULT_DIR}/setu.html" \
        --email \
        --log-cli-level debug



  popd
fi

