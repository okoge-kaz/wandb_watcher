#!/bin/bash

cd /Users/kazuki/Documents/TokyoTech/ylab/test/abci/wandb_watcher
source .env/bin/activate

python run_watcher.py --entity prj-jalm \
  --project Llama-2-7B \
  --run-id "ffvh1mbx" \
  --interval-min 10
