To run the twitter client:
docker run -it -v $PWD:/app --name twitter -w /app python bash
pip install -U git+https://github.com/tweepy/tweepy.git
python twitter_app.py A

Note: Pass in argument "A" for part A, argument "B" for part B.


To run the spark client:
docker run -it -v $PWD:/app --link twitter:twitter eecsyorku/eecs4415
spark-submit spark_app.py A

Note: Pass in argument "A" for part A, argument "B" for part B.


To run the plotter:
python plotter.py A

Note: Pass in argument "A" for part A, argument "B" for part B.