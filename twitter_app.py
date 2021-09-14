import tweepy
import socket
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
    def on_status(self, status):
        for entities in status.entities['hashtags']:
            temp = "#" + entities['text'].lower()
            if(temp in self.track):
                send_tweets_to_spark(temp + "\t" + status.text.replace("\n", " "), self.conn)
                print (temp + "\t" + status.text.replace("\n", " "))


def streamtweets(hashtags,port):
    TCP_IP = "localhost"
    TCP_PORT = port
    conn = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    print("Waiting for TCP connection...")
    conn, addr = s.accept()
    print("Connected... Starting getting tweets.")
    myStreamListener = MyStreamListener()
    MyStreamListener.track = hashtags
    MyStreamListener.conn = conn
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(languages=["en"],track=hashtags)
        
def send_tweets_to_spark(tweet, tcp_connection):
    print("Tweet Text: " + tweet)
    print ("------------------------------------------")
    tcp_connection.send(tweet + '\n')


# streamtweets(['#euro2020','#trump','#delta','#corona','#fashion'],1111)


# resp = streamtweets(['#euro2020','#trump','#delta','#corona','#fashion'],TCP_PORT)
# send_tweets_to_spark(resp, conn)