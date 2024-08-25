## Real-time Marvel Universe Relationship Analyzer

### Objective

Build a system that ingests the Marvel Universe Social Network Dataset, 
processes it in real-time, and provides dynamic relationship analysis between 
characters.

### Components:

Data Ingestion:

 - Use Google Cloud Pub/Sub to simulate real-time data ingestion of character 
   interactions.
 - Create a script to publish dataset entries to a Pub/Sub topic at regular 
intervals.


Data Processing:

 - Use Google Cloud Dataflow to create a streaming pipeline that processes the 
   incoming data.
 - Implement windowing techniques to analyze character relationships over 
   different time periods.

Graph Database:

 - Use Google Cloud Bigtable or a graph database like Neo4j (hosted on Google Compute Engine) to store and query the character relationship data.

Analysis Engine:

 - Develop algorithms to calculate metrics like:
   - Centrality measures (degree, betweenness, eigenvector)
   - Community detection 
   - Shortest paths between characters 
 - Implement these using Apache Beam on Dataflow or with a graph processing 
framework like GraphX.

Real-time API:

 - Create a Cloud Function or deploy a small service on Google Kubernetes
   Engine (GKE) that exposes an API for querying the current state of the 
   Marvel Universe network.

Visualization:

 - Develop a simple web application using Google App Engine that consumes 
   the API and visualizes the Marvel Universe network in real-time.
 - Use a JavaScript library like D3.js or Sigma.js for network visualization.

Monitoring and Logging:

 - Implement comprehensive logging using Google Cloud Logging.
 - Set up monitoring dashboards with Google Cloud Monitoring to track
system performance and data flow.

### Tools used for the project

 - Google Cloud SDK
   - Pub/Sub
   - Dataflow
   - Bigtable
   - Function
   - Monitoring
 - DirectRunner
 - FastAPI

### Languages

 - Python