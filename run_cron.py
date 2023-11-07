import subprocess
import time

while True:
    try:
        # シェルスクリプトを実行
        subprocess.run(["/Users/kazuki/Documents/TokyoTech/ylab/test/abci/wandb_watcher/cron_job_run_watch.sh"], check=True)

        # 10分待機
        time.sleep(600)
    except subprocess.CalledProcessError as e:
        # シェルスクリプトの実行中にエラーが発生した場合、エラーメッセージを出力
        print(f"Error occurred: {e}")
        break
    except KeyboardInterrupt:
        # ユーザーがキーボードで中断した場合、ループを終了
        print("Interrupted by user. Exiting.")
        break
    except Exception as e:
        print(f"Error occurred: {e}")
        break
