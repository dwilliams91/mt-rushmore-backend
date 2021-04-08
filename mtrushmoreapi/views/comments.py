from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from mtrushmoreapi.models import Thread, Comment, RushmoreUser
from django.contrib.auth.models import User



class Comments (ViewSet):
    def list(self, request):
        # add comment for contribution
        all_comments=Comment.objects.all()

        serializer=CommentSerializer(all_comments, many=True, context={'request':request})
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

    # #      {
    # #     "group_id": 1,
    # #     "title":"best cats"
    # # }
    # def destroy(self, request, pk=None):
    #     try:
    #         current_user=RushmoreUser.objects.get(user=request.auth.user)
    #         thread_to_delete=Thread.objects.get(pk=pk, rushmore_user_id=current_user)
    #         thread_to_delete.delete()
    #         return Response({}, status=status.HTTP_204_NO_CONTENT)
    #     except Thread.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=('id', 'rushmore_user_id', 'thread_id', "comment")