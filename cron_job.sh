#!/bin/bash

cd /Users/kazuki/Documents/TokyoTech/ylab/test/abci/wandb_watcher
source .env/bin/activate

python watcher.py --entity llm-jp \
  --project MDS-175B-2023-1005 \
  --interval-min 10
