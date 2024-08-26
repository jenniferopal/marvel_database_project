import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam.io import ReadFromPubSub
from collections import Counter
import json

project_id = "marveldatabaseproject"
topic_name = "marveldatabasetopic"
csv_files = [
    "../marvel_database_project/datasets/edges.csv",
    "../marvel_database_project/datasets/hero-network.csv",
    "../marvel_database_project/datasets/nodes.csv"
]

# parse JSON data from Pub/Sub messages

class ParseJsonFn(beam.DoFn):
    def process(self, element):
        return [json.loads(element.decode('utf-8'))]

# An example of transformation

class FilterCharactersFn(beam.DoFn):
    def process(self, element):
        # Example: Filter characters with more than 5 connections
        if len(element.get('connections', [])) > 5:
            yield element


class MarvelRelationshipTransformFn(beam.DoFn):
    def process(self, element):
        name = element.get('name', 'Unknown')
        connections = element.get('connections', [])
        groups = element.get('groups', [])

        # Count the number of connections
        connection_count = len(connections)

        # Get the top 5 most frequent groups
        top_groups = Counter(groups).most_common(5)

        # Calculate a simple 'relationship strength' metric
        # This could be based on number of shared comics, for example
        relationship_strength = {conn: element.get('shared_comics', {}).get(conn, 0) for conn in connections}

        # Sort connections by relationship strength
        sorted_connections = sorted(relationship_strength.items(), key=lambda x: x[1], reverse=True)
        top_connections = sorted_connections[:5]  # Get top 5 strongest connections

        # Create the transformed element
        transformed_element = {
            'name': name,
            'connection_count': connection_count,
            'top_groups': top_groups,
            'top_connections': top_connections,
            'total_strength': sum(relationship_strength.values()),
            'average_strength': sum(relationship_strength.values()) / len(
                relationship_strength) if relationship_strength else 0
        }

        yield transformed_element

        # Emit relationship pairs for network analysis
        for connected_char, strength in relationship_strength.items():
            yield {
                'character1': name,
                'character2': connected_char,
                'strength': strength
            }

def run():
    # Set up pipeline options
    options = PipelineOptions()
    options.view_as(StandardOptions).streaming = True

    # Create the pipeline
    with beam.Pipeline(options=options) as p:
        # Read from Pub/Sub
        messages = (p | "Read from Pub/Sub" >> ReadFromPubSub(topic="projects/marveldatabaseproject/topics/marveldatabasetopic")
                    | "Parse JSON" >> beam.ParDo(ParseJsonFn())
                    | "Filter Characters" >> beam.ParDo(FilterCharactersFn())
                    | "Print Results" >> beam.Map(print))


if __name__ == '__main__':
    run()
