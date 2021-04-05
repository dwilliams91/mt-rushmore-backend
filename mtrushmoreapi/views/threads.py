from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from mtrushmoreapi.models import Thread

class Threads (ViewSet):
    def list(self, request):
        # add comment for contribution
        all_threads=Thread.objects.all()

        serializer=ThreadSerializer(all_threads, many=True, context={'request':request})
        return Response(serializer.data)

    def create(self,request):
        thread=Thread()
        current_user=User.objects.get(auth_token=request.auth)
        
        thread.title=request.data["title"]
        thread.rushmore_user=current_user
        thread.group=request.data["group"]
        try:
            thread.save()
            serializer=Thread(supply_type, many=False, context={'request':request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model=Thread
        fields=('id', 'rushmore_user_id', 'group_id')