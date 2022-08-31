#!/usr/bin/env bash

cd ~/git/DI-Automation-Scripts/src || exit 1

source diasenv/bin/activate || exit 1

python3 cleanup_instant_clones.py -c ukb.cfg -s || exit 1

exit 0
