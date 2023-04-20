#!/bin/bash
USERMAPPING="--user $(id -u $USER):$(id -g $USER)"

docker run --network=host $USERMAPPING --rm -e USER -e HOME -v $HOME:$HOME -it misato_dataset_doc_uly bash "$@"
