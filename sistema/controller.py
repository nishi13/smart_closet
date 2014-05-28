# -*- coding: utf-8 -*-
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
    saida = '-incluir ou -excluir'
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        lista=cmd.split(' ')
        comando = lista.pop(0)
        if comando == 'incluir':
            roupa = Roupa()
            roupa.cor = lista.pop()
            roupa.tipo = lista.pop()
            roupa.nome = ' '.join(lista)
            roupa.save()
            return HttpResponseRedirect(str(roupa.id) + '/incluirRDIF')
        elif comando == 'excluir':
            nome = ' '.join(lista)
            try:
                roupa = Roupa.objects.get(nome__iexact = nome)
                roupa.delete()
                saida = nome + ' deletado com sucesso'
            except:
                saida = nome + u' não encontrado'

    return render(request, "config_roupa.html", locals())

def config_armario(request):
    saida = 'Deseja -incluir ou -excluir um local'
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        lista=cmd.split(' ')
        comando = lista.pop(0)
        if comando == 'incluir':
            try:
                local = Local()
                local.tipo = lista.pop()
                local.capacidade = int(lista.pop())
                local.nome = ' '.join(lista)
                local.save()
                saida = local.nome + ' salvo com sucesso, Deseja -incluir ou -excluir um local'
            except:
                saida = 'Erro ao tentar salvar, Deseja -incluir ou -excluir um local'
        elif comando == 'excluir':
            nome = ' '.join(lista)
            try:
                local = Local.objects.get(nome__iexact = nome)
                local.delete()
                saida = nome + ' deletado com sucesso, Deseja -incluir ou -excluir um local'
            except:
                saida = nome + u' não encontrado, Deseja -incluir ou -excluir um local'
        elif comando == 'listar':
            saida = ''
            locais = Local.objects.all()
            for local in locais:
                saida += local.nome + ', '
            saida += 'Deseja -incluir ou -excluir um local'

    return render(request, "config_armario.html", locals())

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
        saida = u'Sugestoes: '
        for armario in sugestoes:
            saida += armario.nome + ', '
    else:
        cmd = request.POST.get('comando')
        try:
            armario = Local.objects.get(nome=cmd)
            roupa.local = armario
            roupa.save()
            return HttpResponseRedirect('/configurar/roupa/')
        except:
            saida = 'Error'
    return render(request, "roupa_incluir_local.html", locals())

def vestir(request):
    return render(request, "vestir.html", locals())

def combinacao(request):
    saida = u'Qual a ocasião'
    if request.method == 'POST':


        sugestao = []
        cmd = request.POST.get('comando')
        sugere = Combinacao.objects.filter(ocasiao__iexact = cmd).order_by('-nota')
        print sugere
        for comb in sugere.values() :
            sugestao.append(comb);
        saida = u'Sugestoes: '
        for comb in sugestao:
            saida += comb['nome'] + ','

    return render(request,"combinacao.html",locals())
    #ocasioes = Combinacao.objects.values_list('ocasiao',flat=True)
    #print ocasioes
    #set(ocasioes)
    #for ocasiao in ocasioes :
    #    if (cmd == ocasiao && sugeriu ==0) :
            
    #TODO : erro -> nao existe a ocasiao



    return render(request, "combinacao.html", locals())

def peca(request):
    pass

def guardar(request):
    pass

def mala(request):
    pass

def avaliar(request):
    pass
