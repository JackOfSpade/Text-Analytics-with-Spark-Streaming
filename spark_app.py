import sys
import re
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
# from textblob import TextBlob
import twitter_app

# Initialization operations
def init(hostname, port):
    # A SparkContext represents the connection to a Spark cluster, and can be used to create RDDs. Only one SparkContext should be active per JVM. You must stop() the active SparkContext before creating a new one.
    spark_context = SparkContext(appName="Twitter Stream")

    # Main entry point for Spark Streaming functionality.
    # batchDuration (seconds) - the time interval at which streaming data will be divided into batches. i.e. A batch duration of 1 min tells you that your Spark streaming application works in batches of 1 minute, meaning it plans an RDD every minute.
    streaming_context = StreamingContext(sparkContext=spark_context, batchDuration=1)

    # DStream of the port where the Twitter client is streaming data to.
    DStream = streaming_context.socketTextStream(hostname=hostname, port=port)

    return (streaming_context, DStream)

# Expected data stream format: "#hashtag \t tweet" (without the spaces)
# If a tweet has multiple hashtags, we receive it into Spark multiple times (once with each unique hashtag).
def start_twitter_client(target_hashtags, port):
    twitter_app.streamtweets(target_hashtags, port)

def attach_commands_to_DStream(DStream, hashtags, port, topic=None):
    # Start Twitter client
    start_twitter_client(target_hashtags=hashtags, port=port)

    # If we're doing part A...
    if topic is None:
        # Map: #hashtag \t tweet -----> #hashtag \t 1
        # Reduce: #hashtag \t 1 -----> #hashtag \t total_tweets
        DStream = DStream\
            .map(lambda line: (line.split("\t")[0], 1))\
            .reduceByKey(lambda x, y: x + y)
    # If we're doing part B...
    else:
        # Map: #hashtag \t tweet -----> topic \t [1, sentiment_value]
        # Reduce: topic \t [1, sentiment] -----> topic \t [total_tweets, sentiment_value_list]
        DStream = DStream \
            .map(lambda line: (topic, [1, [get_tweet_sentiment(line.split("\t")[1])]])) \
            .reduceByKey(lambda x, y: [x[0] + y[0], x[1] + y[1]])

    return DStream

# Cleans tweet by removing links, special characters
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    analysis = 1
    # Positive: analysis.sentiment.polarity > 0
    # Neutral: analysis.sentiment.polarity == 0
    # Negative: analysis.sentiment.polarity < 0:
    # return analysis.sentiment.polarity
    return analysis

if __name__ == "__main__":

    # Hashtags for part A:
    vaccine_hashtags = ["#Pfizer", "#Moderna", "#JohnsonAndJohnson", "#AstraZeneca", "#SputnikV"]

    # Topic and Hashtags for part B:
    topic_info = [["Tesla", ["#tesla", "#teslamodel", "#elonmusk", "#teslamotors", "#teslamodels", "#cybertruck",
                      "#teslamodelx", "#teslalife", "#spacex", "#teslaroadster"]],
                  ["Toyota", ["#toyotaclub", "#toyota", "#toyotanation", "#camry", "#toyotalove", "#toyotalife",
                       "#toyotacorolla", "#corolla", "#toyotacamry", "#toyotafamily"]],
                  ["Ford", ["#fords", "#ford", "#fordperformance", "#fordnation", "#fordsofinstagram", "#fordracing",
                       "#mustang", "#mk", "#fordf", "#fordfiesta"]],
                  ["Volkswagen", ["#vw", "#vwlove", "#vwbus", "#vwgolf", "#vwlife", "#vwbeetle", "#vwpolo", "#vwbug",
                       "#vwlovers", "#vwcamper"]],
                  ["Honda", ["#hondas", "#honda", "#hondacivic", "#vtec", "#hondalife", "#civic", "#hondalove",
                             "#hondanation", "#hondatuning", "#hondafest"]]
    ]

    # Put them in a list so we can print or start them together.
    streaming_context_list = []
    DStream_list = []

    # 1st console argument is "A" (do part A):
    if sys.argv[1] == "A":
        # Connect to data stream at specified port
        streaming_context, DStream = init(hostname="localhost", port=2001)
        DStream = attach_commands_to_DStream(DStream=DStream, hashtags=vaccine_hashtags, port=2001)
        DStream_list.append(DStream)
        streaming_context_list.append(streaming_context)
    # # 1st console argument is "B" (do part B)::
    elif sys.argv[1] == "B":
        # Connect to multiple data streams at specified ports
        for i in range(5):
            streaming_context, DStream = init(hostname="localhost", port=2002+i)
            DStream = attach_commands_to_DStream(DStream=DStream, hashtags=topic_info[i][1], port=2002+i, topic=topic_info[i][0])
            DStream_list.append(DStream)
            streaming_context_list.append(streaming_context)
    else:
        print("Error: incorrect argument!")

    for DStream in DStream_list:
        # Print the first ten elements of each RDD generated in this DStream to the console
        DStream.pprint()

    for streaming_context in streaming_context_list:
        # Start the computation
        streaming_context.start()
        # Wait for the computation to terminate
        streaming_context.awaitTermination()
