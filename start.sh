#! /bin/bash
gunicorn --name work_auth --timeout "120" --log-level debug -b 0.0.0.0:1666 -w 4 wsgi:app

