import requests
from bs4 import BeautifulSoup
import json
from pyteaser import SummarizeUrl
import pprint
import time      
import os


class Reuters(object):
	def __init__(self, date):
		self.filename = "reuters_{}.json".format(date)
		self.fn = os.path.join(os.path.dirname(__file__), 'reuters_data_files', self.filename)


	#called in aggregate_Results
	def get_articles(self, category):
		print '...- [processing reuters.com: {}]'.format(category)
		articles = "http://www.reuters.com/news/archive/{}?date=today".format(category)
		r = requests.get(articles)
		soup = BeautifulSoup(r.text)
		a = soup.findAll('div', {'class':'feature'})
		article_links = [x.findAll('a', href=True) for x in a]
		article_links = [item for sublist in article_links for item in sublist]
		article_links = [(x.text, x['href']) for x in article_links]
		article_links = [(x[0],x[1]) for x in article_links if x[1].startswith('/art')]
		article_links = [(x[0],"http://www.reuters.com{}".format(x[1]), " ".join(SummarizeUrl("http://www.reuters.com{}".format(x[1]))).replace('\n','').encode('ascii','ignore')) for x in article_links if x[1].startswith('/art')]
		return article_links


	#called in flatten_reuters_data
	def aggregate_reuters(\
		self,\
		sections={'business': 'businessNews', 'world':'worldNews','politics':'politicsNews','tech':'technologyNews', 'life':'lifestyleMolt'}):
		payload = {'reuters':[]}
		for k,v in sections.items():
			p = self.get_articles(v)
			payload['reuters'].append({'category':k,'articles':p,'date': "{}".format(time.strftime("%Y-%m-%d"))})
		return payload

	def save(self):
		data = self.aggregate_reuters()
		output  = []
		for category in data['reuters']:
			for article in category['articles']:
				output.append(\
					{
						'title':article[0],
						'link':article[1],
						'summary':article[-1][:100]+'...',
						'all': article[-1],
						'category':category['category'],
						'website':'Reuters',
						'date':"{}".format(time.strftime('%Y-%d-%m')),

					})
					


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



class ReutersData(object):
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



		
	









