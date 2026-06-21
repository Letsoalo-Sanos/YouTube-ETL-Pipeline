from airflow import DAG
from datetime import datetime, timedelta
import pendulum
from api.video_stats import get_playlist_id, get_video_ids, extract_video_data, save_to_json

# Define the local timezone
local_tz = pendulum.timezone("Africa/Johannesburg")

# Default Args
default_args = {
    "owner": "dataengineer",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
   # "retries": 1,
    # "retry_delay": timedelta(minutes=5),
    "max_active_runs": 1,
    "dagrun_timeout": timedelta(minutes=60),
    "start_date": datetime(2026, 6, 1, tzinfo=local_tz),
   # "end_date": datetime(2026, 6, 30, tzinfo=local_tz),
}

with DAG(
  dag_id = 'produce_json',
  default_args=default_args,
  description='DAG to produce JSON file with raw data',
  schedule = '0 14 * * *',
  catchup = False
) as dag:
  
  # Define the tasks
  playlistId = get_playlist_id()
  video_ids = get_video_ids(playlistId)
  extracted_data = extract_video_data(video_ids)
  save_json = save_to_json(extracted_data)

  # Define the task dependencies
  playlistId >> video_ids >> extracted_data >> save_json