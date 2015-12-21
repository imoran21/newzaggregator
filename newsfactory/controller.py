from news_sites.reuters.fetch_reuters import Reuters, ReutersData
from news_sites.nyt.fetch_nyt import Nyt, NytData
import time

def get_today():
	return time.strftime("%Y-%m-%d")



def process_reuters():
	reuters = ReutersData()
	reuters.save_today()

def get_reuters_data():
	reuters = ReutersData()
	return reuters.get_data()


def get_nyt_data():
	nyt = NytData()
	return nyt.get_data()



