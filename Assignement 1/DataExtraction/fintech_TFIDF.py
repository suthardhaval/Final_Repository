#source:https://towardsdatascience.com/tfidf-for-piece-of-text-in-python-43feccaa74f8

import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize 
#for IDF calucation using log
import math
import custom_stopwords

# give file path to store data  in variable
filename = 'noisy_text_data.txt'
file = open(filename, 'rt',encoding="UTF-8")
text = file.read()
text = text.lower()
file.close()


def remove_special_characters(s):
	"""
	This function removes the special characters from string
	parameter: s - single input string
	return : stripped string - a string with special characters removed 
	"""
	# remove special chracters with ''
	stripped = re.sub('[^\w\s]','',s)
	stripped = re.sub('_','',stripped)

	#change any whitespace to one space 
	stripped = re.sub('\s+', ' ', stripped)
	#stripped = re.sub("[^a-zA-Z]",'',stripped)
	#remove start & end whitespace
	stripped = stripped.strip()

	return stripped

def get_doc(sent):
	"""
	this function splits the text into sentaces for document consideration
	"""
	doc_info= []
	i=0	
	for sent in text_sents_clean:
		i+=1
		count = count_words(sent)
		temp= {'doc_id' : i, 'doc_length':count}
		doc_info.append(temp)
	return doc_info

def count_words(sent):
	"""
	retuns total number of words in the input text
	"""
	count =0 
	words = word_tokenize(sent)
	for word in words:
		count+=1
	return count

def create_freq_dict(sents):
	"""
	creates dictionary frequency for each document
	"""
	i=0
	frequency_list = []
	for sent in sents:
		i+=1
		frequency_dict ={}
		words = word_tokenize(sent)
		words = [w for w in words if not w in custom_stopwords.stop_words_list]

		for word in words:
			word = word.lower()
			
			if word in frequency_dict:
				frequency_dict[word]+=1
			else:
				frequency_dict[word]=1
			temp ={'doc_id' : i, 'frequency_dict': frequency_dict}
		frequency_list.append(temp)
	return frequency_list

def compute_TF(doc_info, frequency_list):
	"""
	tf = (frequency of the term in doc/total number of terms in docs)
	"""
	TF_Scores = []
	for tempDict in frequency_list:
		id = tempDict['doc_id']
		for k in tempDict['frequency_dict']:
			temp ={'doc_id': id,
					'TF_Score': tempDict['frequency_dict'][k]/doc_info[id-1]['doc_length'],
					'key':k}
			TF_Scores.append(temp)
	return TF_Scores

def compute_IDF(doc_info, frequency_list):
	"""
	idf = ln(total number of docs/number of docs with term in it)
	"""

	IDF_scores = []
	counter =0
	for dict in frequency_list:
		counter+=1
		for k in dict['frequency_dict'].keys():
			count = sum([k in tempDict['frequency_dict'] for tempDict in frequency_dict])
			temp = {'doc_id': counter, 'IDF_scores': math.log(len(doc_info)/count),'key':k}

		IDF_scores.append(temp)
	return IDF_scores


def computeTDIDF(TF_Scores,IDF_scores):
	TFIDF_scores =[]
	for j in IDF_scores:
		for i in TF_Scores:
			if j['key'] == i['key'] and j['doc_id'] == i['doc_id']:
				temp = {'doc_id': j['doc_id'],
						'TFIDF_scores': j['IDF_scores']*i['TF_Score'],
						'key' : i['key']
						}
		TFIDF_scores.append(temp)
	return TFIDF_scores


#cleaer data- remove punctuation and special characters

text_sents = sent_tokenize(text)
text_sents_clean = [remove_special_characters(s) for s in text_sents]
doc_info = get_doc(text_sents_clean)


#calling function for calculations
frequency_dict = create_freq_dict(text_sents_clean)
TF_Scores = compute_TF(doc_info,frequency_dict)
IDF_scores = compute_IDF(doc_info,frequency_dict)
TFIDF_scores = computeTDIDF(TF_Scores,IDF_scores)

print(TFIDF_scores[:10])
#source: https://gis.stackexchange.com/questions/72458/exporting-list-of-values-into-csv-or-txt-file-using-arcpy
#source: https://www.tutorialspoint.com/How-to-save-a-Python-Dictionary-to-CSV-file
import csv
csv_colums =["doc_id","TFIDF_scores","key"]
with open('Fintech_TFIDF.csv', 'w',encoding="UTF-8") as csvFile:
	writer = csv.DictWriter(csvFile,fieldnames = csv_colums)
	writer.writeheader()
	for score in TFIDF_scores:	
    		writer.writerow(score)
csvFile.close()