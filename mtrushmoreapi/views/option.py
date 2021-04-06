from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from mtrushmoreapi.models import Option, Thread, RushmoreUser, Post
from django.contrib.auth.models import User
from rest_framework.decorators import action
from django.forms.models import model_to_dict



class Options (ViewSet):
    def list(self, request):
        # add comment for contribution
        all_options=Option.objects.all()
        print(all_options)

        serializer=OptionSerializer(all_options, many=True, context={'request':request})
        return Response(serializer.data)
    
    def create(self,request):
        option=Option()
        current_user=RushmoreUser.objects.get(user=request.auth.user)
        post=Post()
        thread=Thread.objects.get(id=request.data["thread"])
        post.thread=thread
        post.rushmore_user=current_user

       
        try:
            post.save()
            list_of_options=request.data["options"]
            for item in list_of_options:
                option.post=post
                option.option=item
                option.weight=1
                option.save()



            serializer=Thread(thread, many=False, context={'request':request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

        # {
        #     token:asdfad
        #     thread:1
        #     option1: cheeseburgers,
        #     option2:fries
        #     option3: milkshake
        #     option4:chocolate
        # }
        
        
        

    @action(methods=['get'],detail=True)
    def viewthreadposts(self,request,pk=None):
        
        all_options=Option.objects.filter(post_id__thread_id=pk)
        
        serializer=OptionSerializer(all_options, many=True, context={'request':request})

        return Response(serializer.data)



class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Option
        fields=('id', 'option', 'weight',"post")