from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from sistema.models import *
from django import forms


class InputForm (forms.Form):
    rfid = forms.CharField()
    comando = forms.CharField()


# Create your views here.
def home(request):
    form = InputForm()
    return render(request, "home.html", locals())