#! /bin/bash
gunicorn --name work_auth --timeout "120" --log-level debug -t 3000 -b 0.0.0.0:1666 -w 4 wsgi:app

