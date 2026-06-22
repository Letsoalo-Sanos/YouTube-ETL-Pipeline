import glob
import json
import os
from datetime import date

import logging
logger = logging.getLogger(__name__)

def load_path():

  today_path = f"./data/YouTube_Data_{date.today()}.json"

  if os.path.exists(today_path):
    file_path = today_path
  else:
    candidates = sorted(glob.glob("./data/YouTube_Data_*.json"), reverse=True)
    if not candidates:
      logger.error(f"No YouTube JSON files found in ./data")
      raise FileNotFoundError("No YouTube_Data_*.json files found in ./data")
    file_path = candidates[0]
    logger.warning(
        f"Today's data file not found; falling back to latest available file: {os.path.basename(file_path)}"
    )

  try:
    logger.info(f"Processing file: {os.path.basename(file_path)}")
    with open(file_path, "r", encoding = "utf-8") as raw_data:

      data = json.load(raw_data)

    return data
  except FileNotFoundError:
    logger.error(f"File not found: {file_path}")
    raise
  except json.JSONDecodeError:
    logger.error(f"Error decoding JSON from file: {file_path}")
    raise

def load_data():
  """Backward-compatible alias for older callers expecting `load_data`."""
  return load_path()