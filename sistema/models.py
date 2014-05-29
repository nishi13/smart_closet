from django.db import models

# Create your models here.
class Local(models.Model):
    nome = models.CharField(max_length=128, unique = True)
    capacidade = models.IntegerField()
    tipo = models.TextField(blank=True, null=True)
    @property
    def roupasCount (self):
        return self.roupa_set.count()
    def __unicode__(self):
        return self.nome

class Roupa(models.Model):
    nome = models.CharField(max_length=128)
    local = models.ForeignKey(Local, blank=True, null=True, on_delete=models.SET_NULL)
    rfid = models.CharField(max_length=128, unique = True, blank=True, null=True)
    tipo = models.CharField(max_length=64)
    cor = models.CharField(max_length=64)
    def __unicode__(self):
        return self.nome

class Combinacao(models.Model):
    nome = models.CharField(max_length=128)
    roupas = models.ManyToManyField(Roupa)
    nota = models.IntegerField(default=0)
    aval = models.IntegerField(default=0)
    clima_associado = models.CharField(max_length=128)
    ocasiao = models.CharField(max_length=128)
    data = models.DateTimeField(null = True, blank=True)

    def __unicode__(self):
        return self.nome
