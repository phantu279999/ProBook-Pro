from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from src.common import common


def login_view(request):
	msg = ""
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse('index'))
		else:
			msg = "Your username or password is invalid. Please try again"
	context = {
		"msg": msg
	}
	return render(request, 'accounts/login.html', context=context)


def register_view(request):
	msg = ""
	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		confirm_password = request.POST['confirm_password']
		# check password
		check_pass = common.check_password(password, confirm_password)
		if check_pass is False:
			msg = "Your password can wrong. Please try again"
		else:
			user = User.objects.create_user(username=username, email=email, password=password)
			user.save()
			return HttpResponseRedirect(reverse('accounts:login'))
	context = {
		"msg": msg
	}
	return render(request, 'accounts/register.html', context=context)


@login_required
def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

