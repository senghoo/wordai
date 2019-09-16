#!/bin/bash

service nginx start
uwsgi --ini config/wsgi.ini 

