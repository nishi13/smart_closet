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
    cmd = request.POST.get('comando')
    ocasioes = Combinacao.objects.values_list()
    print ocasioes
    return render(request, "combinacao.html", locals())
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
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        codigo = request.POST.get('rfid')
        if cmd == 'finalizar':
            return HttpResponseRedirect('/')
        else:
            roupaguard = Roupa.objects.get(rfid=codigo)
            localguard = roupaguard.Local;
            return HttpResponseRedirect('/guardar/' + str(roupaguard.id) + '/' + str(localguard.id) + '/guardar_resultado')
    return render(request, "guardar.html", locals())

def guardar_resultado(request, id_roupa, id_local):
    rroupaguard = Roupa.objects.get(id=id_roupa)
    rlocalguard = Local.objects.get(id=id_local)
    saida = 'A peça ' + str(rroupaguard.nome) + 'está no ' + str(rlocalguard.nome) + '.'
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        codigo = request.POST.get('rfid')
        if cmd == 'finalizar':
            return HttpResponseRedirect('/')
        else:
            roupaguard = Roupa.objects.get(rfid=codigo)
            localguard = roupaguard.Local;
            return HttpResponseRedirect('/guardar/' + str(roupaguard.id) + '/' + str(localguard.id) + '/guardar_resultado')
    return render(request, "guardar_resultado.html", locals())

def mala(request):
    pass
    
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
            combav = Combinacao.objects.get(data=datac)
            return HttpResponseRedirect(str(combav.id) + '/avaliar_combinacao')
        elif comando == 'nome':
            nomec = ''
            for parte in lista:
                if nomec:
                    nomec = nomec + '_' + parte
                else:
                    nomec = parte
            print nomec
            combav = Combinacao.objects.get(nome=nomec)
            return HttpResponseRedirect(str(combav.id) + '/avaliar_combinacao')
        else:
            pass
    return render(request, "avaliar.html", locals())
    
def avaliar_combinacao(request, id_combinacao):
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        combav = Combinacao.objects.get(id=id_combinacao)
        avalc = cmd
        combav.aval = avalc
        return HttpResponseRedirect('/avaliar/avaliar_finalizado')
    return render(request, "avaliar_combinacao.html", locals())
   
def avaliar_finalizado(request):
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        if cmd == 'finalizar':
            return HttpResponseRedirect('/')
        else:
            pass
    return render(request, "avaliar_finalizado.html", locals())
    
def combinar(request):
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        lista=cmd.split(' ')
        comando = lista.pop(0)
        if comando == 'criar':
            novaComb = Combinacao()
            novaComb.clima_associado = lista.pop()
            novaComb.ocasiao = lista.pop()
            novaComb.nome = ' '.join(lista)
            return HttpResponseRedirect(str(novaComb.id) +'/combinar_editar')
        else:
           pass
    return render(request, "combinar.html", locals())
    
def combinar_editar(request, id_combinacao):
    if request.method == 'POST':
        editComb = Combinacao.objects.get(id=id_combinacao)
        cmd = request.POST.get('comando')
        lista=cmd.split(' ')
        comando = lista.pop(0)
        if comando == 'incluir':
            enome = ' '.join(lista)
            eroupa = Roupa.objects.get(nome=enome)
            #COMANDO DE INCLUIR ROUPA NA COMBINAÇÃO
            return HttpResponseRedirect(str(novaComb.id) +'/combinar_editar')
        elif comando == 'nota':
            enota = ' '.join(lista)
            editComb.nota = enota
            return HttpResponseRedirect('combinar_finalizado')
        else: 
           pass
    return render(request, "combinar.html", locals())
    
def combinar_finalizado(request):
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        if cmd == 'finalizar':
            return HttpResponseRedirect('/')
        else:
            pass
    return render(request, "combinar_finalizado.html", locals())