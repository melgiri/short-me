#!/bin/bash

FIRST_RUN_MARKER="/.first_run_done"

if [ ! -f "$FIRST_RUN_MARKER" ]; then
  pip3 install -r /root/requirements.txt
  cd /root
  python3 setup.py
  sleep 10
  touch "$FIRST_RUN_MARKER"
  python3 main.py
else
  cd /root
  sleep 10
  python3 main.py
fi
