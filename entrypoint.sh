#!/bin/sh -l

cd /github/workspace/src/DLF
python3 DLFServer.py &
# TODO
# this collection should be updated
#newman run https://www.getpostman.com/collections/12cd4d55bac01c3e06e0
