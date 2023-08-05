#!/bin/bash

if [ -z "$PYPI_USERNAME" ]
then
    echo "PYPI_USERNAME must be provided"
    exit 1
fi

if [ -z "$PYPI_PASSWORD" ]
then
    echo "PYPI_PASSWORD must be provided"
    exit 1
fi

SSH_PATH=${SSH_PATH:-~/.ssh/id_rsa}

docker build \
    --build-arg MATURIN_USERNAME=$PYPI_USERNAME \
    --build-arg MATURIN_PASSWORD=$PYPI_PASSWORD \
    --build-arg ACTION=publish \
    --ssh default=$SSH_PATH \
    .