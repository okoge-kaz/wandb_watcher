#!/bin/bash

cd /Users/kazuki/Documents/TokyoTech/ylab/test/abci/wandb_watcher
source .env/bin/activate

python watcher.py --entity prj-jalm \
  --project Llama-2-13B \
  --interval-min 10
