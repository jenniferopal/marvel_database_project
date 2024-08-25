from google.cloud import pubsub_v1

project_id = "marveldatabaseproject"
topic_name = "marveldatabasetopic"
dataset_path = "../marvel_database_project/datasets/edges.csv"

# Create a publisher client
publisher = pubsub_v1.PublisherClient()

# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_name)

# Data must be a bytestring
data = b"Hello, World!"

# When you publish a message, the client returns a future.
future = publisher.publish(topic_path, data)
print(future.result())