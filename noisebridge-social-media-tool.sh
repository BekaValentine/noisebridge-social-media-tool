#!/bin/bash
cd /home/smt/noisebridge-social-media-tool
source venv/bin/activate
gunicorn --bind 127.0.0.1:3116 slack_integration