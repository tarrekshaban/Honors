import peewee

# Create a connection to the Database
db = peewee.PostgresqlDatabase('honors', user='tshaban')


class Tweet(peewee.Model):
    tweet_id = peewee.BigIntegerField(primary_key=True)
    user_id = peewee.TextField()
    number_of_followers = peewee.IntegerField()
    number_of_tweets = peewee.IntegerField()
    number_of_friends = peewee.IntegerField()
    user_is_verified = peewee.BooleanField()
    language = peewee.TextField()
    tweet_text = peewee.TextField()
    location = peewee.TextField()
    tweet_is_geo = peewee.BooleanField()
    tweet_is_place = peewee.BooleanField()
    place_full_name = peewee.TextField(null=True)
    place_name = peewee.TextField(null=True)
    place_type = peewee.TextField(null=True)
    coordinates = peewee.TextField(null=True)
    tweeted_at = peewee.DateTimeField()
    replying_to_tweet_id = peewee.BigIntegerField()

    class Meta:
        database = db


class Type(peewee.Model):
    type_id = peewee.IntegerField(primary_key=True, unique=True)
    type_name = peewee.TextField()

    class Meta:
        database = db


class Score(peewee.Model):
    tid = peewee.ForeignKeyField(Tweet, related_name='scores')
    score_type = peewee.ForeignKeyField(Type, related_name='scores_of_type')
    score_info = peewee.IntegerField()

    class Meta:
        database = db

if __name__ == "__main__":
    db.connect()
    # Type.create(type_id=0, type_name="Candidate ID - String Match Score")
    # db.drop_tables([Tweet, Score, Type])
    # db.create_tables([Tweet, Score, Type])
    db.close()