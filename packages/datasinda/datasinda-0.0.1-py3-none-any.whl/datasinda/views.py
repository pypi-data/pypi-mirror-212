from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout as django_logout
from django_datasinda import settings

from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from datasinda_backend.serializers import AnalisePCDSerializer

import requests
import json
from ibge.localidades import Estados

def index(request):
    return render(request, 'index.html', {})


url_base = settings.SPADA_HOST
loginSpada = settings.SPADA_LOGIN
passwordSpada = settings.SPADA_PASSWORD

class VerifyEmail(APIView):
    def get(self, request, key):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/api/auth/registration/verify-email/"
        post_data = {'key': key}
        result = requests.post(post_url, data=post_data)
        redirect_url = settings.CORS_ALLOWED_ORIGINS[0]
        return redirect(redirect_url)
    
def getToken():
    usuarioSPADA = {'login' : loginSpada , 'password' : passwordSpada}
    resposta = requests.post(url_base + '/login/entrar', json=usuarioSPADA)
    resp = json.loads(json.dumps(resposta.json()))
    accessToken = 'Bearer ' + resp['access_token']
    return {'Authorization' : accessToken}

@api_view()
@authentication_classes([])
@permission_classes([])
def buscar_todas(request):
    try:
        pcds = requests.get(url_base + '/pcd/todos', headers=getToken())
        pcds_simple = []
        extra_field = ['latitude', 'longitude', 'estado', 'cidade']
        for idx, obj in enumerate(pcds.json()):
            pcd = {'id': obj['id'], 'numero': obj['numero'], 'ativo': obj['ativo'],
                    'proprietario': obj['proprietario']['nome']}
            for field in extra_field:
                if field in obj:
                    pcd[field] = obj[field]
            pcds_simple.append(pcd)
        return JsonResponse(pcds_simple, safe=False)
    except:
        return JsonResponse({'message': 'Erro ao buscar as PCDs'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view()
def buscar_todas_completas(request):
    try:
        pcds = requests.get(url_base + '/pcd/todos', headers=getToken())
        pcds_json = pcds.json()
        for idx, obj in enumerate(pcds_json):
            if 'proprietario' in obj:
                for item in obj['proprietario']:
                    obj['proprietario.' + item] = obj['proprietario'][item]
                del obj['proprietario']
            if 'familiaPCD' in obj:
                for item in obj['familiaPCD']:
                    if item == 'tipoPCD':
                        for item1 in obj['familiaPCD']['tipoPCD']:
                            obj['familiaPCD.tipoPCD.' + item1] = obj['familiaPCD']['tipoPCD'][item1]
                    else:
                        obj['familiaPCD.' + item] = obj['familiaPCD'][item]
                del obj['familiaPCD']
        return JsonResponse(pcds_json, safe=False)
    except:
        return JsonResponse({'message': 'Erro ao buscar as PCDs com todos os metadados'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view()
@authentication_classes([])
@permission_classes([])
def buscar_sensores(request, idPCD):
    try:
        pcd = {'numero' : None, 'id' : idPCD, 'privado' : False, 'cidade' : None,
         'estado' : None, 'proprietario' : None, 'numeroBuscas' : None}
        pcds = requests.post(url_base + '/pcd/buscar/sensores', json=pcd, headers=getToken())
        return JsonResponse(pcds.json(), safe=False)
    except:
        return JsonResponse({'message': 'Erro ao buscar os sensores da PCD'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view()
@authentication_classes([])
@permission_classes([])
def buscar_pcds_publicas(request):
    try:
        pcds = requests.get(url_base + '/pcd/publicas', headers=getToken())
        pcds_json = pcds.json()
        for idx, obj in enumerate(pcds_json):
            if 'familiaPCD' in obj:
                del obj['familiaPCD']
        return JsonResponse(pcds_json, safe=False)
    except:
        return JsonResponse({'message': 'Erro ao buscar as PCDs publicas'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view()
def buscar_pcds_privadas(request):
    try:
        pcds = requests.get(url_base + '/pcd/privadas', headers=getToken())
        pcds_json = pcds.json()
        for idx, obj in enumerate(pcds_json):
            if 'familiaPCD' in obj:
                del obj['familiaPCD']
        return JsonResponse(pcds_json, safe=False)
    except:
        return JsonResponse({'message': 'Erro ao buscar as PCDs privadas'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@swagger_auto_schema(
    methods=['post'],
    request_body=AnalisePCDSerializer)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def buscar_dados(request):
    try:
        analisePCD_data = JSONParser().parse(request)
        pcds = requests.post(url_base + '/analise/pcd/buscar', json=analisePCD_data, headers=getToken())
        return JsonResponse(pcds.json(), safe=False)
    except:
        return JsonResponse({'message': 'Erro ao buscar os dados da PCD'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view()
@authentication_classes([])
@permission_classes([])
def buscar_pcd(request, idPCD):
    try:
        pcds = requests.get(url_base + '/pcd/todos', headers=getToken())
        pcds_json = pcds.json()
        obj = list(filter(lambda x: x['id'] == idPCD, pcds_json))[0]
        extra_field = ['latitude', 'longitude', 'estado', 'cidade']
        pcd_filtered = {'id': obj['id'], 'numero': obj['numero'], 'ativo': obj['ativo'],
                'proprietario': obj['proprietario']['nome']}
        for field in extra_field:
            if field in obj:
                pcd_filtered[field] = obj[field]
        return JsonResponse(pcd_filtered, safe=False)
    except:
        return JsonResponse({'message': 'Erro ao buscar a PCD'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view()
@authentication_classes([])
@permission_classes([])
def buscar_estado(request, estado):
    try:
        pcds_filtered = []
        dados_estados = Estados()
        siglas = dados_estados.getSigla()
        estados = dados_estados.getNome()
        indice_sigla = -1
        for idx, obj in enumerate(siglas):
            if obj == estado:
                indice_sigla = idx
        if indice_sigla == -1:
            return JsonResponse(pcds_filtered, safe=False)
        pcds = requests.get(url_base + '/pcd/todos', headers=getToken())
        pcds_json = pcds.json()
        for idx, obj in enumerate(pcds_json):
            if 'estado' in obj:
                if obj['estado'] == estado or obj['estado'] == estados[indice_sigla]:
                    pcds_filtered.append(obj)
        pcds_simple = []
        extra_field = ['latitude', 'longitude', 'cidade']
        for idx, obj in enumerate(pcds_filtered):
            pcd = {'id': obj['id'], 'numero': obj['numero'], 'ativo': obj['ativo'],
                    'proprietario': obj['proprietario']['nome'], 'estado': obj['estado']}
            for field in extra_field:
                if field in obj:
                    pcd[field] = obj[field]
            pcds_simple.append(pcd)
        return JsonResponse(pcds_simple, safe=False)
    except:
        return JsonResponse({'message': 'Erro ao filtrar as PCDs por estado'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

## func login gov.br
@login_required()
def logout(request):
    try:
        django_logout(request)
    except Exception:
        pass
    url = settings.LOGOUT_URL_GOV_BR
    return HttpResponseRedirect(url)
