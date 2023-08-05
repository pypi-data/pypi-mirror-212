from rest_framework import serializers 


class ProprietarioSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nome = serializers.CharField(max_length=70, allow_blank=True)
    email = serializers.CharField(max_length=180, allow_blank=True)
    cidade = serializers.CharField(max_length=70, allow_blank=True)
    estado = serializers.CharField(max_length=30, allow_blank=True)

class PCDSerializer(serializers.Serializer):
    numero = serializers.IntegerField()
    id = serializers.IntegerField()
    privado = serializers.BooleanField()
    cidade = serializers.CharField(max_length=70, allow_blank=True)
    estado = serializers.CharField(max_length=30, allow_blank=True)
    proprietario = ProprietarioSerializer()
    numeroBuscas = serializers.IntegerField()

class SensoresSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=70, allow_blank=True)
    id = serializers.IntegerField()
        
class AnalisePCDSerializer(serializers.Serializer):
    pcd = PCDSerializer()
    sensores = serializers.ListField(child=SensoresSerializer())
    dataInicial = serializers.DateTimeField()
    dataFinal = serializers.DateTimeField()