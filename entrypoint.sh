#!/bin/sh -l

cd /github/workspace/src/DLF
python3 DLFServer.py &
newman run https://www.getpostman.com/collections/db8c865aca6d4866cdf1
