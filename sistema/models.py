from django.db import models

# Create your models here.
class Local(models.Model):
    nome = models.CharField(max_length=128)
    capacidade = models.IntegerField()
    
    def __unicode__(self):
        return self.nome

class Roupa(models.Model):
    nome = models.CharField(max_length=128,)
    local = models.ForeignKey(Local, blank=True, null=True, on_delete=models.SET_NULL)
    
    def __unicode__(self):
        return self.nome

class Combinacao(models.Model):
    nome = models.CharField(max_length=128)
    roupas = models.ManyToManyField(Roupa)
    nota = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.nome