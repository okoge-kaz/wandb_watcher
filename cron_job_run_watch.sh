#!/bin/bash

cd /Users/kazuki/Documents/TokyoTech/ylab/test/abci/wandb_watcher
source .env/bin/activate

python run_watcher.py --entity prj-jalm \
  --project Llama-2-70B \
  --run-id "g4qo4an6" \
  --interval-min 10
