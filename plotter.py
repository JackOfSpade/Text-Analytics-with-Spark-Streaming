from re import T
import matplotlib.pyplot as plt
import sys

if sys.argv[1] == "A":
    Hashtags = []
    totals = []
    with open(file="spark_output_A.txt", mode = "r") as f: 
        line = f.readline()
        while line :
            print (line)
            #hashtag \t total_tweets
            list1 = line.split("\t")
            Hashtags.append(list1[0])
            totals.append(int(list1[1].replace("\n","")))
            line = f.readline()

    plt.bar(Hashtags, totals)
    plt.title('Hashtags Occurences', fontsize=14)
    plt.xlabel('Hashtags', fontsize=14)
    plt.ylabel('Occurences', fontsize=14)
    plt.ylim([0,max(totals) + 10])
    plt.savefig("output_graph_A")

elif sys.argv[1] == "B":
    topics = []
    totals = []
    sentiments = []
    sentiments_tuples = []
    with open(file="spark_output_B.txt", mode = "r") as f: 
        line = f.readline()
        while line :
            # topic \t [total_tweets, sentiment_value_list]
            list1 = line.split("\t")
            values = list1[1].replace('\n','').replace(']','').replace('[','').split(",")
            topics.append(list1[0])
            totals.append(int(values[0]))
            sentiments.append(values[1:len(values)-1])
            line = f.readline()
    
    for each in sentiments:
        tuple = [0,0,0]
        for i in each:
            if i == '1':
                tuple = [tuple[0],tuple[1],tuple[2]+1]
            elif i == '0':
                tuple = [tuple[0],tuple[1]+1,tuple[2]]
            elif i == '-1':
                tuple = [tuple[0]+1,tuple[1],tuple[2]]
        sentiments_tuples.append(tuple)

    # plt.figure(figsize=(10, 9))
    # i = 0
    # for each in topics:
    #     # plt.bar("Total " + each[0:3], totals[i], width=0.3,color="black")
    #     plt.bar(each[0:5] + " -1", sentiments_tuples[i][0]/totals[i], width=0.3,color="red")
    #     plt.bar(each[0:5] + " 0", sentiments_tuples[i][1]/totals[i], width=0.3,color="grey")
    #     plt.bar(each[0:5] + " 1", sentiments_tuples[i][2]/totals[i],width=0.3,color="green")
    #     i = i + 1
    # plt.xticks(rotation=60)
    # plt.title('Sentiments of Car Companies', fontsize=20)
    # plt.xlabel('Car Company', fontsize=14)
    # plt.ylabel('Percentage', fontsize=14)
    # plt.ylim([0,1])
    # plt.savefig("output_graph_B")

    plt.figure(figsize=(10, 9))
    i = 0
    for each in topics:
        # plt.bar("Total " + each[0:3], totals[i], width=0.3,color="black")
        plt.bar(each[0:5], sentiments_tuples[i][0]/totals[i], width=0.3,color="red")
        plt.bar(' '  + each[0:5], sentiments_tuples[i][1]/totals[i], width=0.3,color="grey")
        plt.bar('  ' + each[0:5], sentiments_tuples[i][2]/totals[i],width=0.3,color="green")
        i = i + 1

    plt.bar(x=[0],height=0,color="green",label="positive")
    plt.bar(x=[0],height=0,color="grey",label="netural")
    plt.bar(x=[0],height=0,color="red",label="negative")

    plt.xticks(rotation=60)
    plt.title('Sentiments of Car Companies', fontsize=20)
    plt.xlabel('Car Company', fontsize=16)
    plt.ylabel('Percentage of Total Tweets', fontsize=16)
    plt.ylim([0,1])
    plt.legend()
    plt.savefig("output_graph_B")