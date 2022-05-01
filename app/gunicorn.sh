#!/bin/sh
gunicorn --chdir app app:app -w 2 --threads 2 -b 127.0.0.1:5000