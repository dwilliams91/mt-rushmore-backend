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


        serializer=OptionSerializer(all_options, many=True, context={'request':request})
        return Response(serializer.data)

    @action(methods=['get'],detail=True)
    def viewThreadPosts(self,request,pk=None):
        print("hi")

        selected_thread=Thread.objects.get(pk=pk)
        all_thread_post=Post.objects.get(thread_id=selected_thread)

        all_options=[]
        for item in all_thread_post:
            option_to_add=Options.objects.filter(post_id=item)
            all_options.append(option_to_add)
        
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