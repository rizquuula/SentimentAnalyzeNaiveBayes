from naiveBayes_preprocessing import preprocessing

text = """
'@jokowi https://t.co/tAn6n84uau
Kasus positif smakin mningkat pak. Dgn PSBB yg cukup ketat aj msih bnyak yg trtular, gmn jdinya dgn NEW NORMAL itu? Yakin ingin mencobanya utk k2 kalinya stlah PSBB?
Tolong pikirkan matang²&amp;jgn coba².
Kami berharap semua KEMBALI NORMAL bukan NEW NORMAL. 🙏'
"""
# text = """'@jokowi pak, kenapa para menteri bapak rebutan bikin peraturan ya, mohon arahan
# https://t.co/qjhjba2HrM
#
# Pengusaha hotel mengharapkan aturan jelas mengenai pelaksanaan new normal pariwisata. Saat ini ada sejumlah poin aturan yang dinilai memberatkan industri.'
# """

result = preprocessing(text)

print(text)
print()
print(result)