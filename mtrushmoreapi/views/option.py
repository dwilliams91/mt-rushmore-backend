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
        current_user=RushmoreUser.objects.get(user=request.auth.user)
        post=Post()
        thread=Thread.objects.get(id=request.data["thread"])
        post.thread=thread
        post.rushmore_user=current_user

       
        try:
            post.save()
            list_of_options=request.data["options"]
            print("list")
            print(list_of_options)
            for item in list_of_options:
                option=Option()
                option.post=post
                option.option=item
                option.weight=1
                option.save()
    # {
    #     "thread":1,
    #     "options":[ "cheeseburgers","french fries","chips","milkshake"]
       
    # }     
            return Response(status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'],detail=True)
    def viewthreadposts(self,request,pk=None):
        
        all_options=Option.objects.filter(post_id__thread_id=pk)
        
        serializer=OptionSerializer(all_options, many=True, context={'request':request})

        return Response(serializer.data)

    @action(methods=['DELETE'],detail=False)
    def deletePost(self,request,pk=None):
        
        try:
            post_to_delete=Post.objects.get(pk=request.data["post_id"])
            options_to_delete=Option.objects.filter(post_id=post_to_delete)
            post_to_delete.delete()
            for item in options_to_delete:
                item.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except post_to_delete.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['PUT'],detail=False)
    def editPost(self,request):
        try:
            post_to_edit=Post.objects.get(pk=request.data["post_id"])
            options_to_edit=Option.objects.filter(post_id=post_to_edit)
            incoming_options=request.data["options"]
            x=-1
            for item in options_to_edit:
                x=x+1
                if item.option not in incoming_options:
                    
                    item.option=incoming_options[x]
                    item.save()

            return Response(status=status.HTTP_201_CREATED)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # {
    #     "options":[ "cheeseburgers","french fries","chips","milkshake"]

    # }
class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Option
        fields=('id', 'option', 'weight',"post")