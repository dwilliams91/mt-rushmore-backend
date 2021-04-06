from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from mtrushmoreapi.models import Option, Thread, RushmoreUser, Post
from django.contrib.auth.models import User
from rest_framework.decorators import action



class Options (ViewSet):
    def list(self, request):
        # add comment for contribution
        all_options=Option.objects.all()
        print(all_options)

        serializer=OptionSerializer(all_options, many=True, context={'request':request})
        return Response(serializer.data)
    

    @action(methods=['get'],detail=True)
    def viewthreadposts(self,request,pk=None):
        print("hello")

        selected_thread=Thread.objects.get(pk=pk)
        all_thread_post=Post.objects.filter(thread_id=selected_thread)

        all_options=[]
        for item in all_thread_post:
            option_to_add=list(Option.objects.filter(post_id=item))
            print(option_to_add[0]__dict__)
            all_options.append(option_to_add)
        
        serializer=OptionSerializer(all_options[1], many=True, context={'request':request})

        return Response(serializer.data)
    

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Option
        fields=('id', 'option', 'weight',"post")