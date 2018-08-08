#!/bin/sh

# run migrate
python3 manage.py makemigrations lunch_foundation
python3 manage.py migrate

# build static
cd frontend
npm install
npm run build
cd ..

python3 manage.py collectstatic --noinput