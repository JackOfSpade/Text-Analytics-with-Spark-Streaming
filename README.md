# Tweet Analytics with Spark Streaming
This application consists of 3 parts:

1. Twitter client (twitter_app.py): This is an application that connects to the Twitter API and obtains tweets as they become available. 

2. Apache Spark Streaming (spark_app.py): This is an apache spark streaming application that connects to our twitter client, receives the tweets as a stream, performs real-time processing of the incoming tweets, extracts useful information, and computes the quantities of interest.

3. Real-time reporting (plotter.py): This is a visualization component that plots the results computed by the apache spark streaming application.

# Example Results
<img src="https://i.imgur.com/LQUFtrF.png" width="75%" height="75%">
<img src="https://i.imgur.com/D3uS08b.png" width="75%" height="75%">
