from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from sistema.models import *
from django import forms

# Create your views here.
def home(request):
    locais = Local.objects.all()
    if len(locais) == 0:
        return HttpResponseRedirect('/configurar/armario')
    return render(request, "home.html", locals())

def configurar(request):
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        lista=cmd.split(' ')
        for item in lista:
            print(item)
    return render(request, "configurar.html", locals())

def config_roupa(request):
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        lista=cmd.split(' ')
        comando = lista.pop(0)
        if comando == 'incluir':
            roupa = Roupa()
            roupa.cor = lista.pop()
            roupa.tipo = lista.pop()
            nome = ''
            for parte in lista:
                if nome:
                    nome = nome + '_' + parte
                else:
                    nome = parte
            roupa.save()
            return HttpResponseRedirect(str(roupa.id) + '/incluirRDIF')
        else:
            pass
    return render(request, "config_roupa.html", locals())

def roupa_incluir_RFID(request, id_roupa):
    if request.method == 'POST':
        roupa = Roupa.objects.get(id=id_roupa)
        cmd = request.POST.get('rfid')
        roupa.rdif = cmd
        roupa.save()
        return HttpResponseRedirect('/configurar/roupa/' + str(roupa.id) + '/local')

    return render(request, "roupa_incluirRFID.html", locals())

def roupa_incluir_local(request, id_roupa):
    roupa = Roupa.objects.get(id=id_roupa)
    if request.method == 'GET':
        armarios = Local.objects.filter(tipo__icontains=roupa.tipo)
        sugestoes = []
        for armario in armarios:
            if armario.capacidade > armario.roupasCount:
                sugestoes.append(armario)
    else:
        cmd = request.POST.get('rfid')
        roupa.rdif = cmd
        roupa.save()
        return HttpResponseRedirect('/configurar/roupa/' + str(roupa.id) + '/local')

    return render(request, "roupa_incluir_local.html", locals())

def avaliar(request):
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        lista=cmd.split(' ')
        comando = lista.pop(0)
        if comando == 'ultima':
            combav = Combinacao.objects.all().order_by('data')[0]
            return HttpResponseRedirect(str(combav.id) + '/avaliar_combinacao')
        elif comando == 'data':
            datac = ''
            for parte in lista:
                if datac:
                    datac = datac + '_' + parte
                else:
                    datac = parte
            combav = combinacao.objects.get(data=datac)
            return HttpResponseRedirect(str(combav.id) + '/avaliar_combinacao')
        elif comando == 'nome':
            nomec = ''
            for parte in lista:
                if nomec:
                    nomec = nomec + '_' + parte
                else:
                    nomec = parte
            combav = combinacao.objects.get(nome=nomec)
            return HttpResponseRedirect(str(combav.id) + '/avaliar_combinacao')
        else:
            pass
    return render(request, "avaliar.html", locals())