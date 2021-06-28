from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import numpy as np

import pandas as pd

import csv, re, operator
# from textblob import TextBlob

app = Flask(__name__)

person = {
	
	'first_name' : '熊',
	'last_name' : '志文',
	'address' : '湖北师范大学',
	'job': '按摩师',
	'tel': '19971522620',
	'email': '931276208@qq.com',
	'github':'xgnzm',
	'blogs':'cnblogs',
	'description' : '我在学习专业知识提高自我科学文化素养的同时，也努力提高自我的思想道德素质，是自我成为德、智、体诸方面全面发展，适应21世纪发展的要求的复合型人才，做一个有思想，有文化，有纪律的社会主义建设者和接班人。',
	'img': 'static/1.jpg',
	'experiences' : [
		{
			'title' : 'Java飞机购票系统',
			'description' : '指导老师：杨**',
			'time' : 'Nov 2018 - 2019'
		},
		{
			'title' : 'Python网页爬虫',
			'description' : '指导老师：李** ',
			'time' : 'Oct 2019-2020'
		},
		{
			'title' : 'pygame飞机大战',
			'description' : '指导老师：李**',
			'time' : 'Dec 2020 - 2021'
		},
		{
			'title' : '教务系统',
			'description' : '指导老师：柯**',
			'time' : 'Dec 2020 - 2021'
		}
	],
	'education' : [
		{
			'university': 'Paris Diderot',
			'degree': 'Projets informatiques et Startégies d\'entreprise (PISE)',
			'description' : 'Gestion de projets IT, Audit, Programmation',
			'mention' : 'Bien',
			'time' : '2015 - 2016'
		},
		{
			'university': 'Paris Dauphine',
			'degree': 'Master en Management global',
			'description' : 'Fonctions supports (Marketing, Finance, Ressources Humaines, Comptabilité)',
			'mention' : 'Bien',
			'timeframe' : '2015'
		},
		{
			'university': 'Lycée Turgot - Paris Sorbonne',
			'degree': 'CPGE Economie & Gestion',
			'description' : 'Préparation au concours de l\'ENS Cachan, section Economie',
			'mention' : 'N/A',
			'timeframe' : '2010 - 2012'
		}
	],
	'programming_languages' : {
		'HMTL' : ['fa-html5', '100'], 
		'CSS' : ['fa-css3-alt', '100'], 
		'SASS' : ['fa-sass', '90'], 
		'JS' : ['fa-js-square', '90'],
		'Wordpress' : ['fa-wordpress', '80'],
		'Python': ['fa-python', '70'],
		'Mongo DB' : ['fa-database', '60'],
		'MySQL' : ['fa-database', '60'],
		'NodeJS' : ['fa-node-js', '50']
	},
	'languages' : {'French' : 'Native', 'English' : 'Professional', 'Spanish' : 'Professional', 'Italian' : 'Limited Working Proficiency'},
	'habbies' : '唱歌、跳舞、打游戏',
	'website':"xyjssb.com"
}

@app.route('/')
def cv(person=person):
	return render_template('index.html', person=person)




@app.route('/callback', methods=['POST', 'GET'])
def cb():
	return gm(request.args.get('data'))
   
@app.route('/chart')
def index():
	return render_template('chartsajax.html',  graphJSON1=gm1(),graphJSON2=gm2(),graphJSON3=gm3(),graphJSON4=gm4(),graphJSON5=gm5())
def gm1():
	df = pd.read_csv('./1.csv',encoding="gbk")
	fig1 = px.density_contour(df,x="日期",y="均价(元)",)
	graphJSON1 = json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON1

def gm2():
	df = pd.read_csv('./1.csv',encoding="gbk")
	fig2 = px.scatter(df,x="日期",y="总市值(元)",color="前收盘价(元)")
	graphJSON2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON2

def gm3():
	df = pd.read_csv('./1.csv',encoding="gbk")
	fig3=px.parallel_categories(df, color="均价(元)", color_continuous_scale=px.
            colors.sequential.Inferno)
	graphJSON3 = json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON3


def gm4():
	df = pd.read_csv('./1.csv',encoding="gbk")
	fig4=px.area(df, x="日期", y="市现率", color="市盈率")
	graphJSON4 = json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON4

def gm5():
	df = pd.read_csv('./1.csv',encoding="gbk")
	fig5=px.histogram(df, x="日期",y="均价(元)",color="市净率", hover_data=df.columns)
	graphJSON5 = json.dumps(fig5,cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON5




@app.route('/senti')
def main():
	text = ""
	values = {"positive": 0, "negative": 0, "neutral": 0}

	with open('ask_politics.csv', 'rt') as csvfile:
		reader = csv.DictReader(csvfile
, delimiter=',', quotechar='"')
		for idx, row in enumerate(reader):
			if idx > 0 and idx % 2000 == 0:
				break
			if  'text' in row:
				nolinkstext = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '', row['text'], flags=re.MULTILINE)
				text = nolinkstext

			blob = TextBlob(text)
			for sentence in blob.sentences:
				sentiment_value = sentence.sentiment.polarity
				if sentiment_value >= -0.1 and sentiment_value <= 0.1:
					values['neutral'] += 1
				elif sentiment_value < 0:
					values['negative'] += 1
				elif sentiment_value > 0:
					values['positive'] += 1

	values = sorted(values.items(), key=operator.itemgetter(1))
	top_ten = list(reversed(values))
	if len(top_ten) >= 11:
		top_ten = top_ten[1:11]
	else :
		top_ten = top_ten[0:len(top_ten)]

	top_ten_list_vals = []
	top_ten_list_labels = []
	for language in top_ten:
		top_ten_list_vals.append(language[1])
		top_ten_list_labels.append(language[0])

	graph_values = [{
					'labels': top_ten_list_labels,
					'values': top_ten_list_vals,
					'type': 'pie',
					'insidetextfont': {'color': '#FFFFFF',
										'size': '14',
										},
					'textfont': {'color': '#FFFFFF',
										'size': '14',
								},
					}]

	layout = {'title': '<b>意见挖掘</b>'}

	return render_template('sentiment.html', graph_values=graph_values, layout=layout)


if __name__ == '__main__':
  app.run(debug= True,port=5000,threaded=True)
