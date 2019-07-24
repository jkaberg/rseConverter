#!/bin/bash

DOCKER_PATH="$(which docker)"
DOCKER_TAG="jkaberg/rseconverter"

INPUT_DIR="$1"
OUTPUT_DIR="$2"

CMD1="${DOCKER_PATH} build --quiet --tag ${DOCKER_TAG} ."

if [[ -d "$INPUT_DIR" ]] && [[ -d "$OUTPUT_DIR" ]] ; then
    CMD2="${DOCKER_PATH} run --rm --volume ${INPUT_DIR}:/input --volume ${OUTPUT_DIR}:/output ${DOCKER_TAG} /input /output ${@:3}"
else
    CMD2="${DOCKER_PATH} run --rm ${DOCKER_TAG} ${@}"
fi

$CMD1
$CMD2
