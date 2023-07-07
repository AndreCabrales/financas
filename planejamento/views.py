from django.shortcuts import render
from perfil.models import Categoria
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def definir_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'definir_planejamento.html', {'categorias': categorias})


@csrf_exempt  # insento o csrftoken do formulário
def update_valor_categoria(request, id):
    # aqui ñ recebo pelo POST.get, pq é uma requisição do javaScript,
    # então recebo como json pela chave definida na function do javaScript
    novo_valor = json.load(request)['novo_valor']

    categoria = Categoria.objects.get(id=id)
    categoria.valor_planejamento = novo_valor
    categoria.save()

    # return HttpResponse(id)
    # return JsonResponse({'valor': f'Recebi o id {id}'})
    return JsonResponse({'status': 'Sucesso'})


def ver_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'ver_planejamento.html', {'categorias': categorias})
