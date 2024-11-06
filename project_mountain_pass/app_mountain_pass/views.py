from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Pass, CustomUser
from .serializers import PassSerializer
from app_mountain_pass.resources import new
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(method='post', request_body=PassSerializer)
@api_view(['POST'])
def submit_data(request):
    serializer = PassSerializer(data=request.data)
    if serializer.is_valid():
        try:
            pass_instance = serializer.save()
            return Response({"status": 200, "message": None, "id": pass_instance.id}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": 500, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({"status": 400, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_pass(request, id):
    try:
        pass_instance = Pass.objects.get(id=id)
        serializer = PassSerializer(pass_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Pass.DoesNotExist:
        return Response({"status": 404, "message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
def edit_pass(request, id):
    try:
        pass_instance = Pass.objects.get(id=id)

        if pass_instance.status != new:
            return Response({"state": 0, "message": "Редактирование запрещено: статус не 'новый'."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PassSerializer(pass_instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"state": 1, "message": "Успешно обновлено."}, status=status.HTTP_200_OK)

        return Response({"state": 0, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Pass.DoesNotExist:
        return Response({"state": 0, "message": "Объект не найден."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def user_passes(request):
    email = request.GET.get('user__email')
    
    if not email:
        return Response({"status": 400, "message": "Email parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    passes = Pass.objects.filter(user__email=email)
    serializer = PassSerializer(passes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)