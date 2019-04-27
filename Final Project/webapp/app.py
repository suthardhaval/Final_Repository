from flask import Flask,render_template,request, url_for, flash, redirect
from forms import SubmitUserDetailsForm
from forms import QuestionsForm
import pandas as pd
import numpy as np
import pickle
import sklearn
import random
from sklearn.svm import SVC
import sys


app = Flask(__name__)
app.config['SECRET_KEY'] = 'f0039cc2d84aa1f4715d1e9e2a413d94'


@app.route('/home', methods = ['POST','GET'])
def index():
	if request.method == 'POST':
		return redirect(url_for('user_details'))
	return render_template('index.html', title = 'index')


@app.route('/user_details', methods = ['POST','GET'])
def user_details():
	if request.method == 'POST':

		id = request.form.get('id')

		file_data = pd.read_csv("uploads/dataset_final.csv")
		dataframe=file_data.loc[file_data['user_id'] == 'user_1', 'user_id':'rank']

		if(dataframe.iloc[0][11] == 'beginner') :
			rank = 1
		if(dataframe.iloc[0][11] == 'intermediate') :
		    rank = 3
		if(dataframe.iloc[0][11] == 'advanced') :
		    rank = 0
		if(dataframe.iloc[0][11] == 'expert') :
		    rank = 2

		df_user = pd.DataFrame({'submission_count':[dataframe.iloc[0][4]],'problem_solved':[dataframe.iloc[0][5]],'contribution':[dataframe.iloc[0][6]],'follower_count':[dataframe.iloc[0][8]],'rating':[dataframe.iloc[0][10]],'rank':[rank]})

		questions_data = pd.read_csv("uploads/problem_data.csv")

		questions_data=questions_data.dropna(subset=['level_type'])

		pkl_filename = "uploads/pickle_model.pkl"

		with open(pkl_filename, 'rb') as file :
			pickle_model = pickle.load(file)

		pickle.load(open(pkl_filename,'rb'))

		list_questions=[]

		random_list=[]


		for key,value in questions_data.iterrows():
		    df_user_local = df_user

		    if(value['level_type'] == 'A') :
		        level_type = 1
		    if(value['level_type'] == 'B') :
		        level_type = 2
		    if(value['level_type'] == 'C') :
		        level_type = 3
		    if(value['level_type'] == 'D') :
		        level_type = 4
		    if(value['level_type'] == 'E') :
		        level_type = 5
		    if(value['level_type'] == 'F') :
		        level_type = 6
		    if(value['level_type'] == 'G') :
		        level_type = 7
		    if(value['level_type'] == 'H') :
		        level_type = 8
		    df_user_local.insert(0,"level_type",level_type)
		    attempt = pickle_model.predict(df_user_local)
		    df_user=df_user.drop('level_type',axis=1)
		    if attempt<=4:
		        list_questions.append(value['problem_id'])

		range = random.randint(0, len(list_questions)-6)

		return render_template('questions.html', len = len(list_questions[:5]), list_questions = list_questions[range:range+5])
	return render_template('user_details.html', title = 'UserDetails')


@app.route('/user_attempts', methods = ['POST','GET'])
def user_attempts():
	if request.method == 'POST':

		id = request.form.get('id')

		level = request.form.get('level')

		file_data = pd.read_csv("uploads/dataset_final.csv")
		dataframe=file_data.loc[file_data['user_id'] == 'user_1', 'user_id':'rank']

		if(dataframe.iloc[0][11] == 'beginner') :
			rank = 1
		if(dataframe.iloc[0][11] == 'intermediate') :
		    rank = 3
		if(dataframe.iloc[0][11] == 'advanced') :
		    rank = 0
		if(dataframe.iloc[0][11] == 'expert') :
		    rank = 2

		df_user = pd.DataFrame({'submission_count':[dataframe.iloc[0][4]],'problem_solved':[dataframe.iloc[0][5]],'contribution':[dataframe.iloc[0][6]],'follower_count':[dataframe.iloc[0][8]],'rating':[dataframe.iloc[0][10]],'rank':[rank]})

		questions_data = pd.read_csv("uploads/problem_data.csv")

		questions_data=questions_data.dropna(subset=['level_type'])

		pkl_filename = "uploads/pickle_model.pkl"

		with open(pkl_filename, 'rb') as file :
			pickle_model = pickle.load(file)

		pickle.load(open(pkl_filename,'rb'))

		list_questions=[]

		if(level == 'A') :
			level_type = 1
		if(level == 'B') :
			level_type = 2
		if(level == 'C') :
			level_type = 3
		if(level == 'D') :
			level_type = 4
		if(level == 'E') :
			level_type = 5
		if(level == 'F') :
			level_type = 6
		if(level == 'G') :
			level_type = 7
		if(level == 'H') :
			level_type = 8

		df_user.insert(0,"level_type",level_type)
		attempt = pickle_model.predict(df_user)
		list_questions.append(attempt)
		print(df_user)

	return render_template('questions.html', len = len(list_questions[:5]), list_questions = list_questions)


# @app.route('/questions', methods = ['GET'])
# def questions():
# 	form = QuestionsForm

# 	return render_template('questions.html', title = 'Questions')

if __name__ == '__main__':
   app.run(debug = True)