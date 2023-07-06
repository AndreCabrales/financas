from django.shortcuts import render, redirect
from django.contrib.messages import constants
from django.contrib import messages
from .models import *
from . utils import calcula_total

# Create your views here.

def home(request):

    contas = Conta.objects.all()

    total_contas = calcula_total(contas, 'valor')

    return render(request, 'home.html', {'contas': contas, 'total_contas': total_contas})

def gerenciar(request):
    contas = Conta.objects.all()
    catagorias = Categoria.objects.all()

    #total_contas = contas.aggregate(Sum('valor'))

    total_conta = 0

    for conta in contas:
        total_conta += conta.valor  

    contex = {
        'contas': contas,
        'total_conta': total_conta,
        'categorias':catagorias,
    }  

    return render(request, 'gerenciar.html', contex)   


def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')
    
    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/perfil/gerenciar/')
    
    conta = Conta(
        apelido = apelido,
        banco=banco,
        tipo=tipo,
        valor=valor,
        icone=icone
    )

    try:
        conta.save()
        messages.add_message(request, constants.SUCCESS, 'Cadastrado com sucesso')
        return redirect('/perfil/gerenciar/')
    except:
        messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
        return redirect('/perfil/gerenciar/')


def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    
    messages.add_message(request, constants.SUCCESS, 'Conta removida com sucesso')
    return redirect('/perfil/gerenciar/')        

def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    categoria = Categoria(
        categoria=nome,
        essencial=essencial
    )

    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')

    return redirect('/perfil/gerenciar/')   

def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)

    categoria.essencial = not categoria.essencial

    categoria.save()

    return redirect('/perfil/gerenciar/')    