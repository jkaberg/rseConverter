#!/bin/bash

set -x

# Parameters to conv.sh
INPUT_FILE=$1
OUTPUT_DIR=$2

# Get base filename and extension
filename=$(basename -- "$INPUT_FILE")
ext="${filename##*.}"
filename="${filename%.*}"

BASE_CMD="/usr/bin/docker run --rm -v ${INPUT_FILE}:/input/${filename}.${ext}:ro -v ${OUTPUT_DIR}:/output:rw jrottenberg/ffmpeg"

# Options we will run FFMPEG with (max 720x406, 30fps)
FFMPEG_OPTS="-c:v mpeg4 -vf scale=720:406:decrease -vtag xvid -qscale:v 2 -c:a libmp3lame -qscale:a 5"

# Make sure output directory exists
mkdir -p "${OUTPUT_DIR}"

# Do conversion
eval "${BASE_CMD} -y -i /input/${filename}.${ext} ${FFMPEG_OPTS} /output/${filename}.avi"
