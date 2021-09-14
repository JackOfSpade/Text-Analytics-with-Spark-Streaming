import tweepy 
import socket
import sys
consumer_key= '2UG5tcU9wD80EXUuVEa5QASbz'
consumer_secret= 'fl7AAy8a5KfbCWcbXZj9PjcAuZc9jkmZCAMOHgrYK5hp5Da2m3'
access_token= '4895214139-uFmmYCvlQ5rkF9l6jahQ3wC5hx8BkS9MNwddwsF'
access_token_secret= 'wtEWjNVS4bSomrFU4MdtsEsPwEjOWjhBg4HsmEKOoniNs'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    track = []
    conn = None
    i = 0
    output = ""
    topic = ""
    def on_status(self, status):
        for entities in status.entities['hashtags']:
            hashtag = "#" + entities['text'].lower()
            if(hashtag in self.track):
                self.output += hashtag + "\t" + status.text.replace("\n", " ") + "\n"
                self.i += 1
                # send_tweets_to_spark(temp + "\t" + status.text.replace("\n", " "), self.conn)
                # print (output)
                if self.i == 10:
                    with open(file="results/output" + self.topic + ".txt", mode = "w") as file_out: 
                        file_out.write(self.output)
                        return
                else:
                    print(str(self.i) + self.output)

            



def streamtweets(hashtags,port):
    # TCP_IP = "localhost"
    # TCP_PORT = port
    # conn = None
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.bind((TCP_IP, TCP_PORT))
    # s.listen(1)
    # print("Waiting for TCP connection...")
    # conn, addr = s.accept()
    # print("Connected... Starting getting tweets.")
    myStreamListener = MyStreamListener()
    MyStreamListener.track = hashtags
    # MyStreamListener.conn = conn
    MyStreamListener.topic = hashtags[0]
    print("topic is: " + MyStreamListener.topic)
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    print("hashtags are: " +  str(hashtags))
    myStream.filter(track=hashtags)

        
def send_tweets_to_spark(tweet, tcp_connection):
    print("Tweet Text: " + tweet)
    print ("------------------------------------------")
    tcp_connection.send(tweet + '\n')

# Hashtags for part A:
vaccine_hashtags = ["#toyotaclub", "#toyota", "#toyotanation", "#camry", "#toyotalove", "#toyotalife",
                       "#toyotacorolla", "#corolla", "#toyotacamry", "#toyotafamily"]

    # Topic and Hashtags for part B:
topic_info = [["Tesla", ["#tesla", "#teslamodel", "#elonmusk", "#teslamotors", "#teslamodels", "#cybertruck",
                      "#teslamodelx", "#teslalife", "#spacex", "#teslaroadster","#pink", "#blue", "#black", "#red", "#yellow", "#euro2020" ]],

                  ["Toyota", ["#toyotaclub", "#toyota", "#toyotanation", "#camry", "#toyotalove", "#toyotalife",
                       "#toyotacorolla", "#corolla", "#toyotacamry", "#toyotafamily"]],
                  ["Ford", ["#fords", "#ford", "#fordperformance", "#fordnation", "#fordsofinstagram", "#fordracing",
                       "#mustang", "#mk", "#fordf", "#fordfiesta"]],
                  ["Volkswagen", ["#vw", "#vwlove", "#vwbus", "#vwgolf", "#vwlife", "#vwbeetle", "#vwpolo", "#vwbug",
                       "#vwlovers", "#vwcamper"]],
                  ["Honda", ["#hondas", "#honda", "#hondacivic", "#vtec", "#hondalife", "#civic", "#hondalove",
                             "#hondanation", "#hondatuning", "#hondafest"]]
]


if sys.argv[1] == "A":
    streamtweets(vaccine_hashtags,8088)
elif sys.argv[1] == "B":
    streamtweets(topic_info[0],8088)
    streamtweets(topic_info[1],8088)
    streamtweets(topic_info[2],8088)
    streamtweets(topic_info[3],8088)
    streamtweets(topic_info[4],8088)

# resp = streamtweets(['#euro2020','#trump','#delta','#corona','#fashion'],TCP_PORT)
# send_tweets_to_spark(resp, conn)