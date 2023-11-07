#!/bin/bash

cd /Users/kazuki/Documents/TokyoTech/ylab/test/abci/wandb_watcher
source .env/bin/activate

python watcher_llama2_70b.py --entity prj-jalm \
  --project Llama-2-70B \
  --interval-min 10
