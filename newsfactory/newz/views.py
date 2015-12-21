from django.shortcuts import render

from controller import get_reuters_data, get_nyt_data

# Create your views here.
def home(request):

	data = get_reuters_data()
	data = data[0]['data']

	ndata = get_nyt_data()
	ndata = ndata[0]['data']
	payload = {
		'reuters_data': data,	
		'nyt_data':ndata,

	}


	return render(request, 'newz/home.html', payload)