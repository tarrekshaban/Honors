from model import *
import datetime
from peewee import *


# Function which returns a list of dates in the DB to use for later quaries
def distinct_dates():
    dates = []
    print "Quarying Dates from DB"
    for tweet in Tweet.select(fn.date_trunc('day', Tweet.tweeted_at)).distinct().dicts():
        dates.append(tweet['date_trunc'])
    print "Finished Quarying Dates from DB"
    return dates


# Function which returns a value 0/1 to determine the time range
# 1: 12:00 AM - 12:00 PM
# 2: 12:00 PM - 12:00 AM
def determine_date(twt):
    dt = twt.tweeted_at
    if dt < dt.replace(hour=12, minute=0, second=0, microsecond=0):
        return 0
    return 1

if __name__ == '__main__':
    dates = distinct_dates()
    for date in dates:
        # Loop four times, once per each score "type"
        print "Working on: " + str(date)
        count0 = 0 # Counter for number of tweets in the first group
        count1 = 0 # Counter for number of tweets in the second group
        for score in range(0, 4):
            # Open files to write in per day
            time_one = open("./data/" + date.strftime('%m-%d-%Y') + "_" + str(score) + ".txt", 'w')
            time_two = open("./data/" + date.strftime('%m-%d-%Y') + "_" + str(score) + ".txt", 'w')
            # Iterate through all the tweets
            for tweet in Tweet.select().join(Score).where((date == fn.date_trunc('day', Tweet.tweeted_at)) & (
                Score.tid_id == Tweet.tweet_id) & (Score.score_type == 0) & (Score.score_info == score)):
                # Process the tweets
                t = tweet.tweet_text.replace('\n', ' ')
                t = ' '.join(t.split())
                # Figure out the time period
                time_period = determine_date(tweet)
                # Write tweet to right time period
                if time_period == 0:
                    # If 12AM - 12PM
                    time_one.write(t.encode("UTF-8")+"\n")
                    count0 += 1
                else:
                    # If 12PM - 12AM
                    time_two.write(t.encode("UTF-8")+"\n")
                    count1 += 1
        print count0, count1
print "Compleated"
