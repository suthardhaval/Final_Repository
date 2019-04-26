from flask import Flask,render_template,request, url_for, flash, redirect
from forms import SubmitSongForm
from googletrans import Translator
from watson_developer_cloud import ToneAnalyzerV3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f0039cc2d84aa1f4715d1e9e2a413d94'

@app.route('/', methods = ['POST','GET'])
def index():
	translator = Translator(service_urls=['translate.google.com'])
	form = SubmitSongForm()
	tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    iam_apikey='0wBNYy4Lb-fO5zLiBJMvN1IDDJP4bHgZhU6MKYSG28zJ',
    url='https://gateway.watsonplatform.net/tone-analyzer/api')
	# if form.validate_on_submit():
	if request.method == 'POST':
		song = form.content.data	
		translation = translator.translate(song)
		text = translation.text
		tone_analysis = tone_analyzer.tone({'text': text},'application/json').get_result()
		tone = tone_analysis.get("document_tone")
		tone = tone.get('tones')
		sad_score=0
		happy_score=0
		analytical_score=0
		tentative_score=0
		for t in tone:
			key = t.get('tone_name')
			value = t.get('score')
			if key == 'Sadness':
				sad_score += value
			elif key == 'Joy':
				happy_score += value
		if sad_score>=happy_score:
			return render_template("result.html",result = "SAD") 
		if happy_score>sad_score:
			return render_template("result.html",result = "HAPPY")
	# return redirect(url_for('result'))
	return render_template('SongPage.html', title = 'SubmitSong', form=form)

if __name__ == '__main__':
   app.run(debug = True)