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

def configurar(request):
    form = InputForm()
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        lista=cmd.split(' ')
        for item in lista:
            print(item)
    return render(request, "configurar.html", locals())

def config_roupa(request):
    form = InputForm()
    return render(request, "config_roupa.html", locals())

def roupa_incluir(request):
    form = InputForm()
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        lista=cmd.split(' ')
        for item in lista:
            print(item)
    return render(request, "roupa_incluir.html", locals())