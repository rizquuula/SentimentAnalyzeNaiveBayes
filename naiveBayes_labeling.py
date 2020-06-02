import sqlite3

def createIdentifiedTable():
    try:
        createTable = """
        CREATE TABLE identifiedData (
           [primary_key] INTEGER PRIMARY KEY NOT NULL,
           [originalTweet] TEXT,
           [preprocessingTweet] TEXT,
           [type] TEXT
        );
        """
        c.execute(createTable)
    except:
        print('pass')
        pass

def insertFromExistingTable(num):
    inserted = """
        INSERT INTO identifiedData(
            primary_key,
            originalTweet,
            preprocessingTweet
            )
        Values(
            {},
            (select originalTweet from jokowiNewNormal where primary_key={}),
            (select preprocessResultTweet from jokowiNewNormal where primary_key={})
            );
    """.format(num, num, num)
    c.execute(inserted)

def transfer():
    c.execute("SELECT originalTweet FROM jokowiNewNormal")
    selectedColumn = c.fetchall()
    primary_id = 1
    for s in selectedColumn:
        insertFromExistingTable(primary_id)
        print(primary_id)
        primary_id+=1

def insertSentimentType(number):
    if number == '1':
        sentiment = "mendukung"
    elif number == '2':
        sentiment = "meragukan"
    elif number == '3':
        sentiment = "menolak"
    elif number == 'quit' or number == '4' or number == '' or number == ' ':
        sentiment = "break"
    else:
        sentiment = "break"
        print("Masukkan hanya nomor 1 atau 2")

    return sentiment

dbPATH = 'jokowidanNewNormal.db'   # PATH
conn = sqlite3.connect(dbPATH)  # konek ke databasenya, kalau belum ada filenya nanti buat sendiri
c = conn.cursor()   # kursor untuk edit database
# createIdentifiedTable()
c.execute("""
    SELECT primary_key FROM identifiedData WHERE type is null or type = ''
    """)
selected = c.fetchall()

# semua data di seleksi berdasarkan primary_key nya
for select in selected:
    # pertama di tampilkan dulu tweet yang akan di identifikasi
    print("*********** {} ***********".format(select[0]))
    print()

    command = "SELECT originalTweet FROM identifiedData WHERE primary_key ={}".format(select[0])
    c.execute(command)
    selectedTweet = c.fetchall()
    print(selectedTweet[0][0])

    command = "SELECT preprocessingTweet FROM identifiedData WHERE primary_key ={}".format(select[0])
    c.execute(command)
    selectedPreprocessingTweet = c.fetchall()

    print()
    print(" ------ Preprocess ------")
    print(selectedPreprocessingTweet[0][0])
    print("")

    # Tahap memasukkan tipe sentimen ke type secara manual
    num = input("Tipe sentimen \n 1) Mendukung 2) Meragukan 3) Menolak : ")
    if insertSentimentType(num) == "break":
        break

    insertType = """
        UPDATE identifiedData SET type='{}' WHERE primary_key ={}  
    """.format(insertSentimentType(num), select[0])
    c.execute(insertType)
    conn.commit()
    print(insertSentimentType(num), select[0])

print("Thanks for your hard work")
c.close()