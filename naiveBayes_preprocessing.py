someStr = """@aniesbaswedan @DKIJakarta @DishubDKI_JKT @TMCPoldaMetro @Puspen_TNI Setiap kali mau lacak status pengajuan selalu seperti ini. Tolong Pak, pengurusan SIKM dibuat mudah. Dengan menunjukkan Surat tugas, Surat domisili &amp; hasil swab sebenarnya sudah cukup. https://t.co/0jwWz3eQai
"""
subjek_dict = "saya aku kamu kita kami mereka kalian dia anda gue gua gw itu ini bang gan"
subjek_dict_konsonan = ['sy', 'k', 'km', 'kt', 'km', 'mrk', 'kln', 'd', 'nd', 'g', 'g', 'gw', 't', 'n', 'bng', 'gn']
vocal_word = ['a', 'i', 'u', 'e', 'o']
symbol = "`1234567890-=~!@#$%^&*()_+{}|[]\;':,./<>?"
symbolList = ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
              '-', '=', '~', '!', '@', '#', '$', '%', '^', '&', '*',
              '(', ')', '_', '+', '{', '}', '|', '[', ']', '\\', ';',
              "'", ':', ',', '.', '/', '<', '>', '?', '''"''']

# preprocessing kalimat
def preprocessing(sentence):
    sentence = sentence.encode('ascii', 'ignore').decode('ascii') # remove all emoji
    sentence = sentence.replace('  ',' ')       # remove double spasi
    sentence = sentence.replace('   ', ' ')     # remove triple spasi
    sentence = sentence.replace('\n', ' ')  # remove enter
    sentence = sentence.replace("'", ' ')  # remove '
    # print(sentence)
    new_sentence = []
    # print(sentence.lower().split(' '))
    for a_word in sentence.lower().split(' '):  # preprocess untuk memisahkan kata-kata di kalimat
        # print(a_word)
        # hilangkan RT (ReTweet)
        if a_word=='rt' or a_word=='' or len(a_word)==1:
            continue

        # koreksi level 1, menghilangkan @
        try:
            if a_word[0] == '@':
                continue
        except:
            # print('except 1')
            pass

        # koreksi menghilangkan link
        try:
            # print(a_word)
            if a_word[0:4] == 'http':
                continue
        except:
            # print('except 2')
            pass

        # koreksi level 2, untuk huruf yang <= 3 langsung lolos
        # dan pengecekan simbol untuk atasi 3 huruf yg jadi kehitung 4 krna ada simbol
        if len(a_word) <= 3 or ((a_word[0] in symbolList or a_word[-1] in symbolList) and len(a_word) == 4):
            if ((a_word[0] in symbolList or a_word[-1] in symbolList) and len(a_word) == 4):
                new_word = []
                for w in a_word:
                    if w not in symbolList:  # hapus semua simbol
                        new_word.append(w)

                new_word_str = ''.join(new_word)
                new_sentence.append(new_word_str)
                continue
            else:
                new_sentence.append(a_word)
                continue

        # koreksi level 3 menghapus huruf vokal dan simbol secara keseluruhan
        new_word = []   # mengisi huruf-huruf konsonan ke list
        for w in a_word:
            if w not in vocal_word and w not in symbolList: # hapus semua huruf vokal
                new_word.append(w)

        new_word_str = ''.join(new_word)
        if new_word_str not in subjek_dict_konsonan and len(new_word_str)>1: # cek supaya ngga ada di subjek
            new_sentence.append(new_word_str)

        # print(new_word_str) # debug kata baru
        del new_word

    # RESULT
    # menggabungkan semuanya jadi satu kalimat utuh
    new_sentence =' '.join(new_sentence) # menggabungkan semua word ke satu sentence dipisahkan pakai spasi

    return new_sentence

# print(preprocessing(someStr))