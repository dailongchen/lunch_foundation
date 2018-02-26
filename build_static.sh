#!/bin/sh

pushd frontend
npm run build
popd

python3 manage.py collectstatic --noinput