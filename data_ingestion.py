import pandas as pd
import json
import time
import os
from google.cloud import pubsub_v1

# Calling Google Cloud creds
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/jenniferopal/gcloud-keys/marveldatabaseproject-mainkey.json"

# Define constants
project_id = "marveldatabaseproject"
topic_name = "marveldatabasetopic"
csv_files = [
    "../marvel_database_project/datasets/edges.csv",
    "../marvel_database_project/datasets/hero-network.csv",
    "../marvel_database_project/datasets/nodes.csv"
]


def read_csv_files(file_paths):
    dataframes = []
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True)


# A function to read and prep the data
def prepare_data(df):
    return df.to_dict(orient='records')


# Function to publish messages to Pub/Sub

def publish_messages(project_id, topic_name, data):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    for record in data:
        message = json.dumps(record).encode('utf-8')
        future = publisher.publish(topic_path, message)
        print(f"Published message id: {future.result()}")
        time.sleep(0.1)  # Add a small delay to simulate real-time data


if __name__ == "__main__":
    # Read and combine all csv files
    combined_data = read_csv_files(csv_files)

    # Prepare the data
    marvel_data = prepare_data(combined_data)

    # Publish messages
    publish_messages(project_id, topic_name, marvel_data)
