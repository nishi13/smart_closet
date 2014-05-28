# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from sistema.models import *
from django.contrib.auth.models import User

locais = [
    {
        'id': 1,
        'nome' : 'gaveta',
        'capacidade': 10,
        'tipo' : 'camiseta shorts cueca camisa',
    },{
        'id': 2,
        'nome' : 'cabide',
        'capacidade': 5,
        'tipo' : 'camiseta blusa camisa',
    },{
        'id': 3,
        'nome' : 'estande',
        'capacidade': 20,
        'tipo' : 'camiseta blusa calca camisa',
    }
]
roupas = [
    {
        'id': 1,
        'nome' : 'Camiseta',
        'local': 1,
        'tipo' : 'camiseta',
        'cor'  : 'azul',
    },{
        'id': 2,
        'nome' : 'Shorts',
        'local': 1,
        'tipo' : 'shorts',
        'cor'  : 'preto',
    },{
        'id': 3,
        'nome' : 'cueca',
        'local': 1,
        'tipo' : 'cueca',
        'cor'  : 'branca',
    },{
        'id': 4,
        'nome' : 'Blusa',
        'local': 2,
        'tipo' : 'blusa',
        'cor'  : 'cinza',
    }
]
combinacoes = [
    {
        'nome' : 'Com Blusa',
        'roupas': [1,2,3,4],
    },{
        'nome' : 'Sem Blusa',
        'roupas': [1,2,3],
    }
]

class Command(NoArgsCommand):
    help = '''Cria Grupos'''
    requires_model_validation = 0

    def handle_noargs(self, **options):

        user = User.objects.create_user('admin', 'admin@admin.com', 'admin')
        user.is_superuser = True
        user.is_staff = True
        user.save()

        for local in locais:
            element = Local(**local)
            element.save()

        for roupa in roupas:
            element = Roupa(id = roupa['id'], nome = roupa['nome'])
            element.local = Local.objects.get(id = roupa['local'])
            element.save()

        for combinacao in combinacoes:
            element = Combinacao(nome = combinacao['nome'])
            element.save()
            element.roupas = Roupa.objects.filter(id__in = combinacao['roupas'])

