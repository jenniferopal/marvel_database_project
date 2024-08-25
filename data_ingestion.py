import pandas as pd
import json
import time
import os
from google.cloud import pubsub_v1

# Calling Google Cloud creds
credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
if not credentials_path:
    raise ValueError("Environment variable GOOGLE_APPLICATION_CREDENTIALS not set.")