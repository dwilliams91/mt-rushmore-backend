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
from difflib import SequenceMatcher
import itertools


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

    @action(methods=['get'],detail=True)
    def findPopularOptions(self,request,pk=None):
        
        all_options=list(Option.objects.filter(post_id__thread_id=pk))
        list_of_options=[]
        for item in all_options:
            one_option=item.__dict__
            list_of_options.append(one_option["option"])

        # remove spaces and hyphens and get everything lower case
        for x in range (0,len(list_of_options)):
            singleItem=list_of_options[x].lower().replace(" ", "").replace("-","").replace("'","")
            # singleItem=singleItem.strip()
            list_of_options[x]=singleItem
        print(list_of_options)

        similarities=[]
        # for x in range (0,len(list_of_options)):
        #     singleItem=list_of_options[x]
        #     for i in range(x+1, len(list_of_options)):
        #         compareItem=list_of_options[i]

        #         if singleItem==compareItem:
        #             similarities.append(singleItem)
        #         if singleItem in compareItem and singleItem not in similarities:
        #             similarities.append(singleItem)
        #         if compareItem in singleItem and compareItem not in similarities:
        #             similarities.append(singleItem)
        # print(similarities)
        
        def find_common_letters(word_1, word_2):
            print(word_1)
            print(word_2)
            
            if len(word_1)>=len(word_2):
                second_word=word_1
                first_word=word_2
            else:
                first_word=word_1
                second_word=word_2
            
            # go through each letter of each word and compare them
            similar_letters=[]
            for x in range(0, len(first_word)):
                if first_word[x]==second_word[x]:
                    similar_letters.append(first_word[x])

            # make a new word of letters in the same position
            new_string=""
            for letter in similar_letters:
                new_string=new_string+letter
            print(new_string)
            

            def find_similar_ratio(a,b):
                return SequenceMatcher(None, a, b).ratio()

            similarRatio=find_similar_ratio(word_1,new_string)
            print(similarRatio)

            if similarRatio>=.85:
                similarities.append(word_1)        

            
        

        for a, b in itertools.combinations(list_of_options, 2):
            find_common_letters(a, b)

        print(similarities)
        
        # go through each letter and compare it to each letter
        # if the letters match, 
                




        serializer=OptionSerializer(all_options, many=True, context={'request':request})

        return Response(serializer.data)

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Option
        fields=('id', 'option', 'weight',"post")