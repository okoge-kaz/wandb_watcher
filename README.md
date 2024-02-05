# wandb_watcher

## usage

Before running, set the following environment variables:

```bash
export SLACK_WEBHOOK_URL=<your slack webhook url>
```

```bash
python watcher.py --entity llm-jp --project MDS-175B-2023-1005
```

```bash
python watcher.py --entity <entity> --project <project>
```

## Watcher usage

Change `https://github.com/okoge-kaz/wandb_watcher/blob/main/cron_job.sh` shell script. and then

```bash
python cron.py
```


## installation

```bash
cd wandb_watcher

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

```
