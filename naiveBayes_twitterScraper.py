import tweepy, sqlite3

def createDB():
    try:
        c.execute("""CREATE TABLE jokowiNewNormal(
                [primary_key] INTEGER PRIMARY KEY NOT NULL,
                [dateTime] TEXT, 
                [id] TEXT, 
                [originalTweet] TEXT,
                [preprocessResultTweet] TEXT,
                [sentimentType] TEXT
                )""")
        print('new (Database/Table created)')
    except:
        print('pass (Database already exist)')
        pass

def insertValue2dB(date, id, text):
    execute = ("""INSERT INTO 
                jokowiNewNormal(
                    dateTime, 
                    id, 
                    originalTweet)
                values(
                    '{}',
                    '{}',
                    '''{}''')""").format(date, id, text)
    # print(execute)
    c.execute(execute)

consumer_key = 'vnY9Rur5SOULbPr5HaJ50bekb'
consumer_secret = 'SOYUsm3x6S6oGUkwBxQV82vCGcIleFlnfdaj62Y5nQ85uOyGYw'
access_token = '1262806974372012033-BTFcBnQ03ir7kVzzsFs1Cs388gy11y'
access_token_secret = 'FNTZjQ7kHR0kAlnQH77RqEwarT2tpe1jE45iTGQygYld7'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# database using sqlite3
dbPATH = 'jokowidanNewNormal.db'
conn = sqlite3.connect(dbPATH)
c = conn.cursor()
createDB()

user_name = "@jokowi"
# user_name = '@aniesbaswedan'
morekeyword = 'new normal'
replies = tweepy.Cursor(api.search, q='to:{} AND {}'.format(user_name, morekeyword),
                                tweet_mode='extended',
                                ).items(1000)
num = 0
for r in replies:
    text = r.full_text.replace("'", '''"''')
    print()
    print(num, r.created_at, r.id, text)
    num+=1
    insertValue2dB(r.created_at, r.id, text)
    conn.commit()

c.close()