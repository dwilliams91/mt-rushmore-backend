from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from mtrushmoreapi.models import Option
from django.contrib.auth.models import User



class Options (ViewSet):
    def list(self, request):
        # add comment for contribution
        all_options=Option.objects.all()

        serializer=OptionSerializer(all_options, many=True, context={'request':request})
        return Response(serializer.data)

    # def create(self,request):
    #     thread=Thread()
    #     # authuser=User.objects.get(auth_token=request.auth)
    #     current_user=RushmoreUser.objects.get(user=request.auth.user)

    #     group=Group.objects.get(pk=request.data["group_id"])
    #     thread.title=request.data["title"]
    #     thread.rushmore_user=current_user
    #     thread.group=group
    #     try:
    #         thread.save()
    #         serializer=Thread(thread, many=False, context={'request':request})
    #         return Response(serializer.data)
    #     except ValidationError as ex:
    #         return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Option
        fields=('id', 'option', 'weight',"post")