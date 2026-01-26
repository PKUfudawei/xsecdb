#!/usr/bin/env python3
import os

for cache in ['datasets.yaml', 'executable', 'condor', 'json']:
    os.system(f'rm -rf {cache}')
