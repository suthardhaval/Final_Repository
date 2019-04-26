# give file path to store data  in variable
filename = 'noisy_text_data.txt'
file = open(filename, 'rt',encoding="UTF-8")
text = file.read()
file.close()

#source:https://machinelearningmastery.com/clean-text-machine-learning-python/
# split into words
from nltk.tokenize import word_tokenize
tokens = word_tokenize(text)
# convert to upper case
tokens = [w.lower() for w in tokens]
# remove punctuation from each word
import string
table = str.maketrans('', '', string.punctuation)
stripped = [w.translate(table) for w in tokens]
# remove remaining tokens that are not alphabetic
words = [word for word in stripped if word.isalpha()]
# filter out stop words
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
words = [w for w in words if not w in stop_words]

#collection package that helps to count the frequency of words
from collections import Counter
word_count = Counter(words).most_common()

#source: https://gis.stackexchange.com/questions/72458/exporting-list-of-values-into-csv-or-txt-file-using-arcpy
import csv
with open('Fintech_words_count.csv', 'w',encoding="UTF-8") as csvFile:
    writer = csv.writer(csvFile, lineterminator='\n')
    writer.writerows(word_count) 
csvFile.close()