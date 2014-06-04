# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from sistema.models import *
from django.contrib.auth.models import User

locais = [
    {
        'id': 1,
        'nome' : 'gaveta1',
        'capacidade': 10,
        'tipo' : 'cueca meia',
    },{
        'id': 2,
        'nome' : 'gaveta2',
        'capacidade': 10,
        'tipo' : 'camiseta',
    },{
        'id': 3,
        'nome' : 'gaveta3',
        'capacidade': 10,
        'tipo' : 'shorts bermuda',
    },{
        'id': 4,
        'nome' : 'cabide1',
        'capacidade': 5,
        'tipo' : 'calca',
    },{
        'id': 5,
        'nome' : 'cabide2',
        'capacidade': 5,
        'tipo' : 'camisa',
    },{
        'id': 6,
        'nome' : 'estante1',
        'capacidade': 20,
        'tipo' : 'blusa',
    }
]

roupas = [
    {
        'id': 1,
        'nome' : 'camisetaLarga',
        'rfid' : 'abc123',
        'local': 2,
        'tipo' : 'camiseta',
        'cor'  : 'branco',
    },{
        'id': 2,
        'nome' : 'camisetaTime',
        'rfid' : 'abc456',
        'local': 2,
        'tipo' : 'camiseta',
        'cor'  : 'vermelho',
    },{
        'id': 3,
        'nome' : 'camisetaRegata',
        'rfid' : 'abc789',
        'local': 2,
        'tipo' : 'camiseta',
        'cor'  : 'preto',
    },{
        'id': 4,
        'nome' : 'camisaSocial',
        'rfid' : 'def123',
        'local': 5,
        'tipo' : 'camisa',
        'cor'  : 'azul',
    },{
        'id': 5,
        'nome' : 'bermudaCasual',
        'rfid' : 'ghi123',
        'local': 3,
        'tipo' : 'bermuda',
        'cor'  : 'azul',
    },{
        'id': 6,
        'nome' : 'shortsCurto',
        'rfid' : 'ghi456',
        'local': 3,
        'tipo' : 'shorts',
        'cor'  : 'preto',
    },{
        'id': 7,
        'nome' : 'calcaSocial',
        'rfid' : 'ghi789',
        'local': 4,
        'tipo' : 'calca',
        'cor'  : 'preto',
   },{
        'id': 8,
        'nome' : 'blusaCorrida',
        'rfid' : 'jkl123',
        'local': 6,
        'tipo' : 'camiseta',
        'cor'  : 'branco',
   },{
        'id': 9,
        'nome' : 'blusaSocial',
        'rfid' : 'jkl456',
        'local': 6,
        'tipo' : 'blusa',
        'cor'  : 'preto',
    }
]

combinacoes = [
    {
        'id': 1,
        'nome' : 'Tipico',
        'roupas': [1,5],
        'ocasiao' : 'Casual',
        'clima_associado' : 'Ameno',
        'nota': 8,
    },{
        'id': 2,
        'nome' : 'Academia',
        'roupas': [1,6,8],
        'ocasiao': 'Casual',
        'clima_associado' : 'Ameno',
        'nota': 6
    },{
        'id': 3,
        'nome' : 'Estadio',
        'roupas': [2,5],
        'ocasiao': 'Casual',
        'clima_associado' : 'Ameno',
        'nota' : 5,
    },{
        'id': 4,
        'nome' : 'Trabalho',
        'roupas': [4,7,9],
        'ocasiao': 'Formal',
        'clima_associado' : 'Frio',
        'nota' : 9,
    },{
        'id': 5,
        'nome' : 'Passeio',
        'roupas': [3,6],
        'ocasiao': 'Praia',
        'clima_associado' : 'Calor',
        'nota' : 7,
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

