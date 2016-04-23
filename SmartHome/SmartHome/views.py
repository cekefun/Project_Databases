from django.shortcuts import render, redirect


def logoutuser(request):
	request.session.flush()
	return redirect('/login/')