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
        'rfid' : 'abc123',
        'local': 1,
        'tipo' : 'camiseta',
        'cor'  : 'azul',
    },{
        'id': 2,
        'nome' : 'Shorts',
        'rfid' : 'abc456',
        'local': 1,
        'tipo' : 'shorts',
        'cor'  : 'preto',
    },{
        'id': 3,
        'nome' : 'cueca',
        'rfid' : 'abc789',
        'local': 1,
        'tipo' : 'cueca',
        'cor'  : 'branca',
    },{
        'id': 4,
        'nome' : 'Blusa',
        'rfid' : 'def123',
        'local': 2,
        'tipo' : 'blusa',
        'cor'  : 'cinza',
    }
]
combinacoes = [
    {
        'id': 1,
        'nome' : 'Calor Com Blusa',
        'roupas': [1,2,3,4],
        'ocasiao' : 'Praia',
        'clima_associado' : 'Chuvoso',
        'nota': 7,
    },{
        'id': 2,
        'nome' : 'Calor Sem Blusa',
        'roupas': [1,2,3],
        'ocasiao': 'Formal',
        'clima_associado' : 'Calor',
        'nota': 6
    },{
        'id': 3,
        'nome' : 'Lindo',
        'roupas': [1,2,3],
        'ocasiao': 'Formal',
        'nota' : 9,
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
            roupas_id = roupa['local']
            del roupa['local']
            element = Roupa(**roupa)
            element.local = Local.objects.get(id = roupas_id)
            element.save()

        for combinacao in combinacoes:
            roupas_id = combinacao['roupas']
            del combinacao['roupas']
            element = Combinacao(**combinacao)
            element.save()
            element.roupas = Roupa.objects.filter(id__in = roupas_id)

