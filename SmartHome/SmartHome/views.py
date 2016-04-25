from django.shortcuts import render, redirect


def logoutuser(request):
	language = request.session["Language"]
	request.session.flush()
	request.session["Language"] = language
	return redirect('/login/')
