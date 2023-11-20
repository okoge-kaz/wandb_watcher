#!/bin/bash

source .env/bin/activate

python watcher_llama2_70b.py --entity prj-jalm \
  --project Llama-2-7B \
  --interval-min 10


python watcher_llama2_70b.py --entity prj-jalm \
  --project Llama-2-13B \
  --interval-min 10

python watcher_llama2_70b.py --entity prj-jalm \
  --project Llama-2-70B \
  --interval-min 10
