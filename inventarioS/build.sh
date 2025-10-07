#!/usr/bin/env bash
set -o errexit

pip install -r inventarioS/requirements.txt

python inventarioS/manage.py collectstatic --no-input

python inventarioS/manage.py migrate
