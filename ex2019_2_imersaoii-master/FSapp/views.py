from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import *
from .models import Imersionista, Ponto, Evento
from .sendemail import send, sendlink
from datetime import datetime,timedelta, date
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import qrcode
import smtplib

# Create your views here.


def cadastro(request):
    form = ImersionistaForm(request.POST or None, request.FILES or None)
    if form.is_valid():

        form.save()
        return HttpResponseRedirect(reverse('confirma_cadastro', args=[form.cleaned_data['matricula']]))
    return render(request, 'cadastro.html', {'form': form})

def confirma_cadastro(request, matricula):
    imersionista = get_object_or_404(Imersionista, pk=matricula)
    matriculap = imersionista.matricula
    matriculap = str(matriculap)
    img = qrcode.make(matriculap)
    img.save('media/qrcode/'+matriculap+'.png')

    send(imersionista.email, matriculap)

    return render(request, 'confirma_cadastro.html', {'imersionista': imersionista})


def logout_view(request):
    logout(request)
    return redirect('inicio')

def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect("dashboard")

    if request.POST:
        form = LoginVeterano(request.POST)
        if form.is_valid():
            matricula = request.POST['matricula']
            password = request.POST['password']
            user = authenticate(matricula=matricula, password=password)

            if user:
                login(request, user)
                return redirect("dashboard")
    else:
        form =  LoginVeterano()

    return render(request, 'account/login.html', {'form':form})


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required(login_url='login')
def rankingpalestra(request):
    pessoas = Imersionista.objects.all()
    pessoas_sorted = sorted(pessoas, key=Imersionista.get_horapalestra, reverse=True)
    return render(request, 'ranking.html', {'pessoas_sorted': pessoas_sorted})


@login_required(login_url='login')
def rankingworkshop(request):
    pessoas = Imersionista.objects.all()
    pessoas_sorted = sorted(pessoas, key=Imersionista.get_horaworkshop, reverse=True)

    matricula = request.POST.get('matricula', default=0)
    escolha = request.POST.get('desafio',default=1)
    for imersionista in pessoas:
        if imersionista.matricula == int(matricula):
            imersionista.notadesafio = int(escolha)
            imersionista.save()

            break

    print(type(matricula))
    print(escolha)
    return render(request, 'rankingworkshop.html', {'pessoas_sorted': pessoas_sorted})

@login_required(login_url='login')
def rankinggeral(request):

    pessoas = Imersionista.objects.all()
    pessoas_sorted = sorted(pessoas, key=Imersionista.get_horastotal, reverse=True)

    return render(request, 'rankinggeral.html', {'pessoas_sorted':pessoas_sorted} )

@login_required(login_url='login')
def leitorqr(request):
    evento = Evento.objects.last()
    if not evento:
        return redirect('criar_evento')
    return render(request, 'leitorqr.html')

@login_required(login_url='login')
def baterponto(request, matricula):
    mat = int(matricula)
    imersionistas = Imersionista.objects.all()
    individuo = 0
    for imersionista in imersionistas:
        if imersionista.matricula == mat:
            individuo = get_object_or_404(Imersionista, pk=mat)
            break
    if individuo == 0:
        return JsonResponse({'message': 'Qrcode inválido! ' + str(matricula)})

    pontos = Ponto.objects.all()
    listadepontos = []
    for ponto in pontos:
        if ponto.imersionista.matricula == mat:
            listadepontos.append(ponto)

    #variavel tamanho é o tamanho da lista de pontos, e para acessarmos o ultimo elemento, usaremos tamanho - 1
    tamanho = len(listadepontos)

    # aqui batemos o ponto, verificando se o ultimo ponto q ele bateu está como hora de saida, senão bate a hora de saida
    # se sim, cria um ponto novo com hora de entrada.
    if listadepontos:
        if not listadepontos[tamanho - 1].saida:
            listadepontos[tamanho - 1].saida = datetime.now().strftime('%H:%M:%S')

            evento = Evento.objects.last()

            even = ((datetime.strptime(str(date.today()), "%Y-%m-%d")) - (datetime.strptime(str(evento.workshop), "%Y-%m-%d"))).days






            # Aqui verificamos se o imersionista bate o ponto antes da hora setada ali na linha abaixo, se sim deleta, se não adiciona
            horat = '14:00:00'
            formatohora = '%H:%M:%S'
            if (datetime.strptime(horat, formatohora) -
                datetime.strptime(listadepontos[tamanho - 1].saida,
                                  formatohora)).total_seconds() > 0:
                listadepontos[tamanho - 1].delete()

            else:
                dif = round((datetime.strptime(str(listadepontos[tamanho-1].saida), formatohora) -
                                      datetime.strptime(str(listadepontos[tamanho-1].entrada), formatohora)).total_seconds()/60,0)
                if even < 0:
                    ponto.evento = "Palestra"
                    imersionista.horaspalestra += dif

                else:
                    ponto.evento = "Workshop"
                    imersionista.horasworkshop += dif

                imersionista.horastotal += dif
                imersionista.save()
                listadepontos[tamanho - 1].save()

        else:
            ponto = Ponto(imersionista=individuo, entrada=datetime.now().strftime('%H:%M:%S'),
                          data=datetime.today())

            ponto.save()

    else:
        ponto = Ponto(imersionista=individuo, entrada=datetime.now().strftime('%H:%M:%S'),
                      data=datetime.today())
        ponto.save()

    return JsonResponse({'message': 'Ponto Batido: ' + str(matricula)})


@login_required(login_url='login')
def criar_evento(request):
    form = EventoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'evento.html', {'form': form})


def area_interesse(request):
    matriculab = request.POST.get('matricula',default=0)
    escolhadeinteresse = request.POST.get('AREADEINTERESSE', default='Area')
    print (escolhadeinteresse)
    imersionistas = Imersionista.objects.all()

    try:
        matriculab = int(matriculab)
    except Exception as e:
        print(e)

    for imersionista in imersionistas:
        if imersionista.matricula == matriculab:
            imersionista.areadeinteresse = escolhadeinteresse
            print(imersionista.areadeinteresse)
            print(escolhadeinteresse)
            imersionista.save()

            break


    return render(request, "areadeinteresse.html")







@login_required(login_url='login')
def enviarlink(request):
    imersionistas = Imersionista.objects.all()
    lista = []
    for imersionista in imersionistas:
        lista.append(imersionista.email)

    #DEpois que tivermos o url correto, corrigiremos essa view para enviar o link correto

    sendlink(lista)
    return render(request, 'dashboard.html')