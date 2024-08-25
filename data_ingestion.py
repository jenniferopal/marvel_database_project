import pandas as pd
import json
import time
import os
from google.cloud import pubsub_v1

# Variables

file_path = "../marvel_database_project/datasets/edges.csv"

# Calling Google Cloud creds
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/jenniferopal/gcloud-keys/marveldatabaseproject-mainkey.json"

# Define constants

project_id = "marveldatabaseproject"
topic_name = "marveldatabasetopic"
dataset_path = "../marvel_database_project/datasets/edges.csv"


# A function to read and prep the data

def prepare_data(dataset_path):
    df = pd.read_csv(dataset_path)
    return df.to_dict(orient='records')

# Function to publish messages to Pub/Sub

def publish_messages(project_id, topic_name, dataset_path):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    for record in dataset_path:
        message = json.dumps(record).encode('utf-8')
        future = publisher.publish(topic_path, message)
        print(f"Published message id: {future.result()}")
        time.sleep(1)  # Add a small delay to simulate real-time data


if __name__ == "__main__":
    # Prepare the data
    marvel_data = prepare_data(dataset_path)

    # Publish messages
    publish_messages(project_id, topic_name, dataset_path)
