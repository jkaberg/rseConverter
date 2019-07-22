#!/bin/bash

DOCKER_PATH="$(which docker)"
DOCKER_TAG="jkaberg/rseconverter"

INPUT_DIR="$1"
OUTPUT_DIR="$2"

CMD1="${DOCKER_PATH} build -t ${DOCKER_TAG} ."
CMD2="${DOCKER_PATH} run --rm -v ${INPUT_DIR}:/input -v ${OUTPUT_DIR}:/output ${DOCKER_TAG} /input /output ${@:3}" 

$CMD1
$CMD2
