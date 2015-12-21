import requests
from bs4 import BeautifulSoup
import json
from pyteaser import SummarizeUrl
import pprint
import time      
import os


class Nyt(object):
	def __init__(self, date):
		self.filename = "nyt_{}.json".format(date)
		self.fn = os.path.join(os.path.dirname(__file__), 'nyt_data_files', self.filename)


	#called in aggregate_Results
	def get_articles(self, category):
		print '...- [processing nyt.com: {}]'.format(category)
		articles = "http://www.nytimes.com/section/{}".format(category)
		r = requests.get(articles)
		soup = BeautifulSoup(r.text)
		latest = soup.find('section', {'id':'latest-panel'})
		latest = latest.findAll('div', {'class':'story-body'})
		articles = []
		for article in latest:
			text = " ".join(SummarizeUrl(article.find('a', {'class': 'story-link'})['href']))

			text = text.encode('ascii', 'ignore').replace("\n","")

			temp = {}
			temp.update({'category':'world'})
			temp.update({'website':'NYT'})
			temp.update({'title':article.find('h2', {'class': 'headline'}).text.strip()})
			temp.update({'link': article.find('a', {'class': 'story-link'})['href'] })
			temp.update({'date':'{}'.format(time.strftime("%Y-%m-%d"))})
			
			temp.update({'summary': "{}...".format(text[:100])})
			temp.update({'all':text})

			articles.append(temp)


		return articles
			


	#called in flatten_reuters_data
	def aggregate_nyt(\
		self,\
		sections={'business': 'businessNews', 'world':'world','politics':'politicsNews','tech':'technologyNews', 'life':'lifestyleMolt'}):
		payload = {'reuters':[]}
		for k,v in sections.items():
			p = self.get_articles(v)
			payload['reuters'].append({'category':k,'articles':p,'date': "{}".format(time.strftime("%Y-%m-%d"))})
		return payload

	def save(self):
		data = self.get_articles('world')
		output = []
		output.append({'data':{}})
		output[0]['data'].update({'world':data})
					
		with open(self.fn, 'wb') as f:
			json.dump(output, f, indent=4)
			print '{} scraped'.format(f)

	def get_data(self):
		if os.path.isfile(self.fn):
			with open(self.fn, 'rU') as f:
				data = json.load(f)
			return data
		else:
			raise ValueError, 'File does not exist: {}'.format(self.fn)
	def exists(self):
		return os.path.isfile(self.fn)



class NytData(object):

	def __init__(self):
		self.fp = os.path.join(os.path.dirname(__file__), 'nyt_data_files')

	def get_data(self):
		with open(os.path.join(self.fp, 'categorized.json'), 'rU') as f:
			return json.load(f)



'''

class NYTData(object):
	def __init__(self):
		self.fp = os.path.join(os.path.dirname(__file__), 'reuters_data_files')

	def aggregate_files(self):
		output = []
		files = [x for x in os.listdir(self.fp) if x.startswith('reuters_')]
		for fn in files:
			with open(os.path.join(self.fp, fn), 'rU') as f:
				output+= json.load(f)
		return output

	def save_all(self):
		with open(os.path.join(self.fp, 'master.json'), 'wb') as f:
			json.dump(self.aggregate_files(), f, indent=4)

	def save_today(self):

		r = Reuters(time.strftime("%Y-%m-%d"))
		if r.exists():
			print '!-= Todays data already obtained=-!'
		else:
			r.save()
		
		self.save_all()
		print '-= master rebuild =-'
		self.transform_data()
		print '-= data categorized =-'

	def get_raw_data(self):
		with open(os.path.join(self.fp, 'master.json'), 'rU') as f:
			return json.load(f)

	def transform_data(self):
		categorized={'business': [], 'world':[],'politics':[],'tech':[], 'life':[]}
		data = self.get_raw_data()
		for x in data:
			categorized[x['category']].append(x)
		with open(os.path.join(self.fp,'categorized.json'), 'wb') as f:
			json.dump([{'data':categorized}], f, indent=4)

	def get_data(self):
		with open(os.path.join(self.fp, 'categorized.json'), 'rU') as f:
			return json.load(f)



		
	


'''






