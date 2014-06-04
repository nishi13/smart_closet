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
    saida = ''
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
    saida = ''
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
                saida = '"' + local.nome +'" salvo com sucesso.'
            except:
                saida = 'Erro ao tentar salvar.'
        elif comando == 'excluir':
            nome = ' '.join(lista)
            try:
                local = Local.objects.get(nome__iexact = nome)
                local.delete()
                saida = '"' + nome + '" deletado com sucesso.'
            except:
                saida = '"' + nome + u'" não encontrado.'
        elif comando == 'listar':
            saida = ''
            locais = Local.objects.all()
            for local in locais:
                saida += local.nome + ', '
            saida += ''

    return render(request, "config_armario.html", locals())

def roupa_incluir_RFID(request, id_roupa):
    roupa = Roupa.objects.get(id=id_roupa)
    saida = '"' + roupa.nome +'" salvo com sucesso.'
    if request.method == 'POST':
        cmd = request.POST.get('rfid')
        roupa.rfid = cmd
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
    saida = u'Qual e a ocasião?'
    if request.method == 'POST':
        print cmd
        try:
            sugere = list(Combinacao.objects.filter(ocasiao__iexact = cmd).order_by('-nota'))
            return HttpResponseRedirect( '/vestir/combinacao/' + str(sugere[0].id) + '/combinacao_finalizado')
        except: saida = u'Ocasiao inexistente. Digite uma ocasiao valida.'
    return render(request,"combinacao.html",locals())

def combinacao_finalizado(request,id_comb):
    sugestao = Combinacao.objects.get(id=id_comb)
    saida = u'Sugestão: "' + str(sugestao) + '", que consiste em: '
    roupas = list(sugestao.roupas.all())
    for roupa in roupas :
        saida += '"' + str(roupa) + '", '
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        if cmd == 'recusar':
            return HttpResponseRedirect('/vestir/combinacao/' + str(sugestao.id) + '/recusar')
        elif cmd =='aceitar':
            retirada = []
            l = len(roupas)
            for ret in roupas :
                 retirada.append(str(ret.id))
            fazer = '_'.join(retirada)
            return HttpResponseRedirect( '/vestir/combinacao/' + ''.join(fazer) + '/retirar')
    return render(request, "combinacao_finalizado.html", locals())

def retirar(request,itera):
    iteracao = itera.split('_')
    roupa = Roupa.objects.get(id=iteracao.pop(0))
    saida = '"' +str(roupa.nome) + u'" está em "' + str(roupa.local) + '".'
    itera = '_'.join(iteracao)
    print itera
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        if cmd == 'proximo':
            if len(itera) >0 :
                return HttpResponseRedirect('/vestir/combinacao/'+ itera + '/retirar')
            else :
                return HttpResponseRedirect('/')
    return render(request, "retirar.html", locals())

def recusar(request,id_comb):
    primsugest = Combinacao.objects.get(id=id_comb)
    novasugest = Combinacao.objects.get(id=id_comb)
    #saida = ''
    saida = 'Nova combinacao encontrada. '
    saida += u'Sugestão: "' + str(novasugest) + '", que consiste em: '
    roupas = list(novasugest.roupas.all())
    for roupa in roupas :
        saida += '"' + str(roupa) + '", '
    listasug = list(Combinacao.objects.filter(ocasiao__iexact = primsugest.ocasiao).order_by('-nota'))
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        lista=cmd.split(' ')
        comando = lista.pop(0)
        if comando == 'filtro':
            tipof = lista.pop(0)
            param = ' '.join(lista)
            rfiltro = 0
            listasug = list(Combinacao.objects.filter(ocasiao__iexact = primsugest.ocasiao, ).order_by('-nota'))
            for combinacao in listasug:
                roupas = list(combinacao.roupas.all())
                for roupa in roupas:
                    if rfiltro == 0:
                        if tipof == 'nome':
                            if roupa.nome == param:
                                novasugest = combinacao
                                rfiltro = 1
                        if tipof == 'tipo':
                            if roupa.tipo == param:
                                novasugest = combinacao
                                rfiltro = 1
                        if tipof == 'cor':
                            if roupa.cor == param:
                                novasugest = combinacao
                                rfiltro = 1
            if rfiltro == 1:
                saida = 'Nova combinacao encontrada. '
                saida += u'Sugestão: "' + str(novasugest) + '", que consiste em: '
                roupas = list(novasugest.roupas.all())
                for roupa in roupas :
                    saida += '"' + str(roupa) + '", '
                return HttpResponseRedirect('/vestir/combinacao/' + str(novasugest.id) + '/recusar')
            else:
                novasugest = primsugest
                saida = 'Nao foi possivel encontrar uma nova sugestao com esse filtro. Tente novamente.'
        elif comando == 'aceitar':
            roupas = list(novasugest.roupas.all())
            retirada = []
            l = len(roupas)
            for ret in roupas :
                 retirada.append(str(ret.id))
            fazer = '_'.join(retirada)
            return HttpResponseRedirect( '/vestir/combinacao/' + ''.join(fazer) + '/retirar')
        else:
            pass
    return render(request, "recusar.html", locals())

def peca(request):
    saida = ''
    retirar =[]
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        lista=cmd.split(' ')
        comando = lista.pop(0)
        identificacao = ' '.join(lista)
        if comando == 'escolher':
            try:
                roupa = Roupa.objects.get(nome=identificacao)
                saida = '"' + identificacao + u'" está em "' + str(roupa.local) + '".'
            except:
                saida = '"' + identificacao + '" nao foi encontrado.'
        elif comando == 'finalizar' :
            return HttpResponseRedirect('/')
    return render(request,"peca.html", locals())

def guardar(request):
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        codigo = request.POST.get('rfid')
        if cmd == 'finalizar':
            return HttpResponseRedirect('/')
        else:
            roupaguard = Roupa.objects.get(rfid=codigo)
            localguard = roupaguard.local;
            return HttpResponseRedirect('/guardar/' + str(roupaguard.id) + '/' + str(localguard.id) + '/guardar_resultado')
    return render(request, "guardar.html", locals())

def guardar_resultado(request, id_roupa, id_local):
    rroupaguard = Roupa.objects.get(id=id_roupa)
    rlocalguard = Local.objects.get(id=id_local)
    saida = 'A peça ' + str(rroupaguard.nome) + ' deve ser guardada em ' + str(rlocalguard.nome) + '. '
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        codigo = request.POST.get('rfid')
        if cmd == 'finalizar':
            return HttpResponseRedirect('/')
        else:
            roupaguard = Roupa.objects.get(rfid=codigo)
            localguard = roupaguard.local;
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
            datac = ' '.join(lista)
            combav = Combinacao.objects.get(data=datac)
            return HttpResponseRedirect(str(combav.id) + '/avaliar_combinacao')
        elif comando == 'nome':
            nomec = ' '.join(lista)
            combav = Combinacao.objects.get(nome=nomec)
            return HttpResponseRedirect(str(combav.id) + '/avaliar_combinacao')
        else:
            pass
    return render(request, "avaliar.html", locals())

def avaliar_combinacao(request, id_combinacao):
    combav = Combinacao.objects.get(id=id_combinacao)
    saida = 'Avaliar combinacao "' + combav.nome +'".'
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        avalc = cmd
        combav.aval = avalc
        combav.save()
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
            novaComb.save()
            return HttpResponseRedirect(str(novaComb.id) +'/combinar_editar')
        else:
           pass
    return render(request, "combinar.html", locals())

def combinar_editar(request, id_combinacao):
    saida = 'Editar combinacao.'
    if request.method == 'POST':
        editComb = Combinacao.objects.get(id=id_combinacao)
        cmd = request.POST.get('comando')
        lista=cmd.split(' ')
        comando = lista.pop(0)
        if comando == 'incluir':
            enome = ' '.join(lista)
            eroupa = Roupa.objects.get(nome=enome)
            editComb.roupas.add(eroupa)
            editComb.save()
            saida = '"' + str(eroupa.nome) + '" adicionada a combinacao "' + str(editComb.nome) + '". '
        elif comando == 'nota':
            enota = ' '.join(lista)
            editComb.nota = enota
            editComb.save()
            saida = '"' +(editComb.nome) + '" avaliada com nota ' + str(editComb.nota) + '. '
            return HttpResponseRedirect('/combinar/' +str(id_combinacao) +'/combinar_finalizado')
        else:
           pass
    return render(request, "combinar_editar.html", locals())

def combinar_finalizado(request, id_combinacao):
    if request.method == 'POST':
        cmd = request.POST.get('comando')
        if cmd == 'finalizar':
            return HttpResponseRedirect('/')
        else:
            pass
    return render(request, "combinar_finalizado.html", locals())
