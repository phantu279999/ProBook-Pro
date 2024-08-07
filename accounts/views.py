from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from . import models


def login_view(request):
	if request.method == 'POST':
		username = request.GET['username']
		password = request.GET['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse('index'))

	return render(request, 'accounts/login.html')


def register_view(request):

	if request.method == 'POST':
		username = request.GET['username']
		email = request.GET['email']
		password = request.GET['password']
		comfirm_password = request.GET['comfirm_password']
		# check password

		user = models.User.objects.create_user(username=username, email=email, password=password)
		user.save()
		return HttpResponseRedirect(reverse('accounts:login'))

	return render(request, 'accounts/register.html')


@login_required
def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

