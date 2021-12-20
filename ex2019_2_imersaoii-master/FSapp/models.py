from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .validators import *
from datetime import datetime
from django.core.validators import MinLengthValidator, MinValueValidator, RegexValidator, MaxValueValidator


class ControleImersionista(BaseUserManager):
    def _create_user(self, matricula,password, first_name, last_name, cpf, email, curso, is_staff, is_admin, is_superuser, **extrasfields):

        if not cpf:
            raise ValueError('CPF deve ser especificado')
        if not matricula:
            raise ValueError('Matricula deve ser especificado')

        user = self.model(
            matricula=matricula,
            first_name=first_name,
            last_name=last_name,
            cpf=cpf,
            email=email,
            curso = curso,
            is_staff=is_staff,
            is_admin=is_admin,
            is_superuser=is_superuser,
            **extrasfields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user


    def create_user(self, matricula, first_name, last_name, cpf, email, curso, periodo, anexo_1, anexo_2, anexo_3, **extrafields):
        return self._create_user(matricula, first_name, last_name, cpf, email, curso, periodo, anexo_1, anexo_2, anexo_3, False, False, False, **extrafields)

    def create_superuser(self, matricula,password, first_name, last_name, cpf, email, curso, **extrafields):
        user = self._create_user(matricula, password, first_name, last_name, cpf, email, curso, True, True, True, **extrafields)

        user.save(using=self._db)
        return user


class Imersionista(AbstractBaseUser):
    numeric = RegexValidator(r'^[0-9]*$', 'Only numeric characters are allowed.')

    matricula = models.IntegerField(blank=False, null=False, primary_key=True, verbose_name="Matrícula ",  validators = [MinValueValidator(1000000000, "Menos de 10 digitos"), MaxValueValidator(9999999999, "Mais de 10 digitos") ])
    first_name = models.CharField(max_length=30, blank=False, null=False, verbose_name="Primeiro Nome ")
    last_name = models.CharField(max_length=30, blank=False, null=False, verbose_name="Sobrenome ")
    cpf = models.CharField(max_length=12, blank=False, null=False,validators = [numeric, MinLengthValidator(11, 'menos de 11 digitos')], verbose_name='CPF ')
    email = models.EmailField(max_length=60, blank=False, null=False, verbose_name='Email ')

    Curso_Tipo = [
        ('C', 'Ciência da computação'),
        ('S', 'Sistemas para internet'),
        ('G', 'Gestão da TI'),
        ('R', 'Redes de computadores'),
        ('O', 'Outros'),
    ]
    curso = models.CharField(max_length=1, choices=Curso_Tipo, default="Outros")
    periodo = models.CharField(max_length=1, blank=True, null=True)

    anexo_1 = models.ImageField(null=True, verbose_name="Identidade")
    anexo_2 = models.ImageField(null=True, verbose_name="Horário Individual")
    anexo_3 = models.ImageField(null=True, verbose_name="Comprovante de Matrícula")
    horaspalestra = models.IntegerField(blank=True, default=0)
    horasworkshop = models.IntegerField(blank=True, default=0)
    horastotal = models.IntegerField(blank=True, default=0)
    notadesafio = models.IntegerField(blank = True, default=1)

    Area_Tipo= [
        ('BackEnd', 'BACKEND'),
        ('FrontEnd', 'FRONTEND'),
        ('Analise de Requisitos', 'ANALISTA REQ'),
        ('Banco de Dados', 'BD'),
        ('Devops', 'DEVOPS'),
        ('Jogos', 'JOGOS'),
        ('Gestão de Projetos', 'GP'),
        ('Testes', 'TESTES'),
        ('Desenvolvimento Mobile', 'MOBILE'),
        ('Business Intelligence', 'Business Intelligence'),
        ('Area', 'NÃO ESCOLHEU'),
    ]

    areadeinteresse = models.CharField(max_length=30, choices=Area_Tipo, default="Area")

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'matricula'
    REQUIRED_FIELDS = ['cpf', 'email', 'first_name', 'last_name', 'curso', 'periodo']

    objects = ControleImersionista()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def get_horapalestra(self):
        return self.horaspalestra

    def get_horaworkshop(self):
        return self.horasworkshop

    def get_horastotal(self):
        return self.horastotal

    def __str__(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_Label):
        return True

class Ponto(models.Model):
    evento = models.CharField(max_length=20, null=True, blank=True)
    data = models.DateField(blank=False, null=False)
    saida = models.TimeField(blank=True, null=True)
    entrada = models.TimeField(blank=True, null=True)
    #id_ponto = models.IntegerField(primary_key=True, blank=False, null=False)
    #horario_total = models.CharField(max_length=50, blank=True, null=True)
    imersionista = models.ForeignKey('Imersionista',on_delete=models.CASCADE)



    def __str__(self):
        NomePonto = (str(self.imersionista.first_name) + ' - ' + (str(self.data)))
        return NomePonto


class Evento(models.Model):
    workshop = models.DateField(verbose_name="Workshop")



