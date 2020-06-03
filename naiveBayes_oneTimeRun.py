import sqlite3, numpy
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

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
merged = mendukung[:jumlahData] + menolak[:jumlahData]
x_train = []
for x in range(len(merged)):
    x_train.append(merged[x][0])

y_train = []

for i in range(jumlahData):
    y_train.append('mendukung')
for x in range(jumlahData):
    y_train.append('menolak')

print(numpy.array(x_train).shape)
print(numpy.array(y_train).shape)

count_vect = CountVectorizer()
x_train_counts = count_vect.fit_transform(x_train)
print(x_train_counts.shape)
# print(count_vect.vocabulary_.get(u'nrml')) # menghitung berapa banyak kata tertentu
#  “Term Frequency times Inverse Document Frequency”
tf_transform = TfidfTransformer(use_idf=False).fit(x_train_counts)
x_train_tf = tf_transform.transform(x_train_counts)
print(x_train_tf.shape)

model = MultinomialNB().fit(x_train_tf, y_train)

# Try to predict
benar = 0
salah = 0

jumlahData = 0

for testData in mendukung[jumlahData:]:
    # testData = (meragukan[32])
    test_new_counts = count_vect.transform(testData)
    tf_transform = TfidfTransformer(use_idf=False).fit(test_new_counts)
    test_new_tf = tf_transform.transform(test_new_counts)
    predicted_as = model.predict(test_new_tf)
    print(predicted_as)
    if predicted_as=='mendukung':
        benar += 1
    else:
        salah += 1

for testData in menolak[jumlahData:]:
    # testData = (meragukan[32])
    test_new_counts = count_vect.transform(testData)
    tf_transform = TfidfTransformer(use_idf=False).fit(test_new_counts)
    test_new_tf = tf_transform.transform(test_new_counts)
    predicted_as = model.predict(test_new_tf)
    print(predicted_as)
    if predicted_as=='menolak':
        benar += 1
    else:
        salah += 1

print("benar = ", benar)
print("salah = ", salah)
print("persentase benar = ", 100*benar/(benar+salah))
c.close()