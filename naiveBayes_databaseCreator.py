from naiveBayes_preprocessing import preprocessing
import sqlite3

dbPATH = 'jokowidanNewNormal.db'   # PATH
conn = sqlite3.connect(dbPATH)  # konek ke databasenya, kalau belum ada filenya nanti buat sendiri
c = conn.cursor()   # kursor untuk edit database
c.execute("SELECT originalTweet FROM jokowiNewNormal")
selectedTweets = c.fetchall()
num = 1
c.close()
c = conn.cursor()   # kursor untuk edit database

for tweet in selectedTweets:
    # print('-    -    -')
    # print(tweet[0])
    proctweet = preprocessing(tweet[0])
    execute = ("""REPLACE INTO jokowiNewNormal(
                    primary_key, 
                    dateTime,
                    id,
                    originalTweet,
                    preprocessResultTweet
                    ) 
                    values(
                    {},
                    (select dateTime from jokowiNewNormal where primary_key={}),
                    (select id from jokowiNewNormal where primary_key={}),
                    (select originalTweet from jokowiNewNormal where primary_key={}),
                    '{}'
                    )""").format(num, num, num, num, proctweet)
    # print('--------------------------')
    # print(execute)
    # print('- - - - -')
    print(num, proctweet)
    c.execute(execute)
    num += 1

conn.commit()

# text = """
# '@jokowi https://t.co/tAn6n84uau
# Kasus positif smakin mningkat pak. Dgn PSBB yg cukup ketat aj msih bnyak yg trtular, gmn jdinya dgn NEW NORMAL itu? Yakin ingin mencobanya utk k2 kalinya stlah PSBB?
# Tolong pikirkan matang²&amp;jgn coba².
# Kami berharap semua KEMBALI NORMAL bukan NEW NORMAL. 🙏'
# """
# # text = """'@jokowi pak, kenapa para menteri bapak rebutan bikin peraturan ya, mohon arahan
# # https://t.co/qjhjba2HrM
# #
# # Pengusaha hotel mengharapkan aturan jelas mengenai pelaksanaan new normal pariwisata. Saat ini ada sejumlah poin aturan yang dinilai memberatkan industri.'
# # """
#
# result = preprocessing(text)
#
# print(text)
# print()
# print(result)