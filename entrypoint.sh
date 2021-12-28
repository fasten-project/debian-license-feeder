#!/bin/sh -l

cd /github/workspace/src/DLF
python3 DLFServer.py &
# this collection has been updated, it contains 1 GET and 1 test
newman run https://www.getpostman.com/collections/db8c865aca6d4866cdf1
