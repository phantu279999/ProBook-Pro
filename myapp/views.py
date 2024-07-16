import os
import sys

from django.shortcuts import render

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.process.process_seo import ProcessSEO

def index(request):
	context = {}
	if request.method == 'POST':
		your_domain = request.POST['your_domain']
		res = ProcessSEO().process_single_link(your_domain)
		context['res'] = res
	return render(request, 'index.html', context=context)

