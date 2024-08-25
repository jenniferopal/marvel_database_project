import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam.io import ReadFromPubSub
from apache_beam.io.gcp.bigquery import WriteToBigQuery
import json

# Define constants

project_id = "marveldatabaseproject"
topic_name = "marveldatabasetopic"
subscription = "projects/marveldatabaseproject/subscriptions/marveldatabasetopic-sub ".format(project_id, 'marveldatabasetopic-sub')
dataset_path = "../marvel_database_project/datasets/edges.csv"

# Schema for your BigQuery table

schema = {
    'fields': [
        {'name': 'hero', 'type': 'STRING'},
        {'name': 'comic', 'type': 'STRING'},
    ]
}

# Pipeline steps
class ParsePubSubMessage(beam.DoFn):
    def process(self, element):
        message = json.loads(element.decode('utf-8'))
        yield {
            'hero': message['hero'],
            'comic': message['comic'],
        }

def run():
    # Set up the pipeline options
    options = PipelineOptions(
        runner = 'DataflowRunner',
        project = project_id,
        job_name = 'marvel-universe-pipeline',
        temp_location = 'gs://your-bucket/temp',
        region = 'your-region'
    )
    options.view_as(StandardOptions).streaming = True


