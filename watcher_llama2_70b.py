import argparse
import json
import os
import re
from datetime import datetime

import pytz  # type: ignore
import requests  # type: ignore
import wandb
from wandb.apis.public import Run


def get_current_runnings(entity: str, project: str) -> list[Run]:
    runs: list[Run] = wandb.Api().runs(
        path=f"{entity}/{project}",
    )
    current_runnings: list[Run] = []

    for run in runs:
        if run.state == "running":
            current_runnings.append(run)
    return current_runnings


def arg_parser() -> argparse.Namespace:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--entity", type=str, required=False, default="prj-jalm")
    parser.add_argument("--project", type=str, required=False, default="Llama-2-70B")
    parser.add_argument("--interval-min", type=int, required=False, default=10)
    args = parser.parse_args()
    return args


def get_last_line(filename: str) -> str:
    with open(filename, "r") as f:
        lines: list[str] = f.readlines()

    index: int = -1
    last_line: str = lines[index] if lines else ""
    while "step" not in last_line:
        index -= 1
        last_line = lines[index]

    return last_line


def extract_last_timestamp_and_step(last_run: str) -> tuple[str, int]:
    datetime_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
    step_pattern = r"(\d+) step"

    time_match = re.search(datetime_pattern, last_run)
    step_match = re.search(step_pattern, last_run)

    if time_match:
        time_extracted = time_match.group(1)
        print("Time:", time_extracted)

    if step_match:
        step_extracted = int(step_match.group(1))
        print("Steps:", step_extracted)

    return time_extracted, step_extracted  # type: ignore


def send_slack_alert(alert_message: str) -> None:
    headers: dict[str, str] = {"Content-type": "application/json"}
    data: dict[str, str] = {"text": alert_message}
    response = requests.post(
        url=os.environ["SLACK_WEBHOOK_URL"],
        headers=headers,
        data=json.dumps(data),
    )

    print(f"LOG: slack response: {response}")


def main() -> None:
    args = arg_parser()

    if "SLACK_WEBHOOK_URL" not in os.environ:
        with open(".config", "r") as f:
            os.environ["SLACK_WEBHOOK_URL"] = f.read().strip()
        print("DEBUG: slack : ", os.environ["SLACK_WEBHOOK_URL"])

    runs = get_current_runnings(entity=args.entity, project=args.project)
    if len(runs) == 0:
        raise ValueError("No running run found")
    print(f"LOG: currently running: {runs[0].id}, {runs[1].id}, ...")

    # mkdir
    os.makedirs(name=".wandb_watcher_cache", exist_ok=True)
    cache_runs: list[str] = os.listdir(path=".wandb_watcher_cache")

    for run in runs:
        step: int = run.summary.get("_step", 0)
        timestamp: float = run.summary.get("_timestamp", 0)
        human_readable_timestamp: str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

        if run.id not in cache_runs:
            os.makedirs(name=f".wandb_watcher_cache/{run.id}")
            with open(f".wandb_watcher_cache/{run.id}/last_run", mode="a") as f:
                f.write(f"{human_readable_timestamp}: {step} step\n")
            print("LOG: first run")
        else:
            last_run: str = get_last_line(filename=f".wandb_watcher_cache/{run.id}/last_run")
            if last_run == "":
                print("LOG: last run is not found")
                with open(f".wandb_watcher_cache/{run.id}/last_run", mode="a") as f:
                    f.write(f"{human_readable_timestamp}: {step} step\n")
                exit(0)

            print(f"LOG: last run: {last_run}")

            last_run_time, last_run_step = extract_last_timestamp_and_step(last_run=last_run)

            if last_run_step == step:
                print("LOG: no update")
                now = datetime.now(pytz.timezone("Asia/Tokyo"))
                elapsed_time: float = now.timestamp() - timestamp
                print(f"LOG: elapsed time: {elapsed_time} seconds")
                if elapsed_time > 60 * args.interval_min:
                    print(f"LOG: no update for {args.interval_min} minutes. maybe something wrong. exit")
                    send_slack_alert(
                        alert_message=f"❌: CAUTION: no update for {args.interval_min} minutes.\nmaybe something wrong.\n last iteration: {last_run_step}, last update: {last_run_time}"
                    )
            else:
                print("LOG: updated")
                with open(f".wandb_watcher_cache/{run.id}/last_run", mode="a") as f:
                    f.write(f"{human_readable_timestamp}: {step} step\n")
                # send_slack_alert(alert_message=f"updated 🎉\n last iteration: {last_run_step}")


if __name__ == "__main__":
    main()
