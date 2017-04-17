#!/bin/bash
set -o allexport

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..

if [ -e .env ]; then
	source .env
fi
echo $OMARTESTPY2_DOCKER_IMAGE_LOCAL

docker build -t $OMARTESTPY2_DOCKER_IMAGE_LOCAL:$OMARTESTPY2_IMAGE_VERSION . 
