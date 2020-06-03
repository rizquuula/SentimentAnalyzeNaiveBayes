import sqlite3, numpy
import random
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

def trainingNaiveBayes(x_train, y_train):
    # print(x_train.shape, y_train.shape)
    count_vect = CountVectorizer()
    x_train_counts = count_vect.fit_transform(x_train)
    # print(x_train_counts.shape)
    # print(count_vect.vocabulary_.get(u'nrml')) # menghitung berapa banyak kata tertentu
    #  “Term Frequency times Inverse Document Frequency”
    tf_transform = TfidfTransformer(use_idf=False).fit(x_train_counts)
    x_train_tf = tf_transform.transform(x_train_counts)
    # print(x_train_tf.shape)

    model = MultinomialNB().fit(x_train_tf, y_train)

    return model, count_vect

dbPATH = 'jokowidanNewNormal.db'   # PATH
conn = sqlite3.connect(dbPATH)  # konek ke databasenya, kalau belum ada filenya nanti buat sendiri
c = conn.cursor()   # kursor untuk edit database

c.execute("""
    SELECT preprocessingTweet FROM identifiedData WHERE type = 'mendukung'
    """)
mendukung = c.fetchall()
print("Jumlah data mendukung = ", numpy.array(mendukung).shape) # (43, 1)

c.execute("""
    SELECT preprocessingTweet FROM identifiedData WHERE type = 'menolak'
    """)
menolak = c.fetchall()
print("Jumlah data menolak = ", numpy.array(menolak).shape) # (50, 1)

jumlahData = 150
print("jumlah data training = ", jumlahData)
merged = mendukung[:jumlahData] + menolak[:jumlahData] # data training
testDatabase = mendukung[0:] + menolak[0:] # data testing
testDatabase = random.sample(testDatabase, len(testDatabase))

x_test = []
for x in range(len(testDatabase)):
    x_test.append(testDatabase[x][0])
# x_test = shuffle(x_test)
print('test database = ', numpy.array(x_test).shape)

x_train = []
for x in range(len(merged)):
    x_train.append(merged[x][0])
print('x_learn database = ', numpy.array(x_train).shape)

y_train = []
for i in range(jumlahData):
    y_train.append('mendukung')
for x in range(jumlahData):
    y_train.append('menolak')
print('x_learn database = ', numpy.array(y_train).shape)

# Try to predict
benar = 0
salah = 0
# count_vect = CountVectorizer()
# Iterasi data testing

for data in x_test:
    model, count_vect = trainingNaiveBayes(x_train, y_train)
    # print("data is = ", data)
    # Data yang diambil selanjutnya
    data_new_counts = count_vect.transform([data])

    tf_transform = TfidfTransformer(use_idf=False).fit(data_new_counts)
    data_new_tf = tf_transform.transform(data_new_counts)
    predicted_as = model.predict(data_new_tf)[0]

    # Ambil data sebenarnya dari sqlite database untuk dicocokkan
    fetchData = """
        SELECT type FROM identifiedData WHERE preprocessingTweet = '{}'
    """.format(data)
    c.execute(fetchData)
    isTrueType = c.fetchall()[0][0]
    ####

    if predicted_as == isTrueType:
        benar += 1
        sign = '=='
    else:
        salah += 1
        sign = '!='

    print(predicted_as, ' {} '.format(sign), isTrueType)
    x_train.append(data[0])
    y_train.append(predicted_as)


print("benar = ", benar)
print("salah = ", salah)
print("persentase benar = ", 100*benar/(benar+salah))
c.close()