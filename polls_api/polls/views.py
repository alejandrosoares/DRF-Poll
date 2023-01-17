from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404

from utils.constants import MAX_SIZE_ITEMS
from utils.authentication import BasicAuthentication
from utils.permissions.permission import IsAdmin, IsPollster
from .models import Poll, Choice, Vote
from .serializers import (
    PollSerializer, 
    PollCreateSerializer, 
    ChoiceSerializer, 
    VoteSerializer
)
from .utils.constants import DELETE_PERMISSION_DENIED, CREATE_PERMISSION_DENIED
from .utils.permissions import is_own_or_raise_exception

def poll_list(request):
    polls = Poll.objects.all()[:MAX_SIZE_ITEMS]
    data = PollSerializer(polls, many=True).data
    return JsonResponse(data , safe=False)

def poll_detail(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    data = PollSerializer(poll).data
    return JsonResponse(data)

# class PollList(APIView):
#     def get(self, request):
#         polls = Poll.objects.all()[:MAX_SIZE_ITEM]
#         data = PollSerializer(polls, many=True).data
#         return Response(data)

# class PollDetail(APIView):
#     def get(self, request, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         data = PollSerializer(poll).data
#         return Response(data)

class PollListView(BasicAuthentication,
                generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & (IsAdmin | IsPollster)]
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class PollCreateView(BasicAuthentication,
                    generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Poll.objects.all()
    serializer_class = PollCreateSerializer              

class PollDetailDeleteView(BasicAuthentication, 
                        generics.RetrieveDestroyAPIView):

    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def __get_creator_id(self):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        return poll.created_by.id

    def delete(self, request, *args, **kwargs):
        creator_id = self.__get_creator_id()
        user_id = request.user.id
        is_own_or_raise_exception(user_id, creator_id, DELETE_PERMISSION_DENIED)
        super().delete(request, *args, **kwargs)

class ChoiceListCreateView(BasicAuthentication,
                        generics.ListCreateAPIView):

    serializer_class = ChoiceSerializer
    
    def __get_creator_id(self):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        return poll.created_by.id

    def get_queryset(self):
        choices = Choice.objects.filter(poll__id=self.kwargs['pk'])
        return choices

    def post(self, request, *args, **kwargs):
        creator_id = self.__get_creator_id()
        user_id = request.user.id
        is_own_or_raise_exception(user_id, creator_id, CREATE_PERMISSION_DENIED)
        super().post(request, *args, **kwargs)

class VoteListCreateView(BasicAuthentication,
                        generics.ListCreateAPIView):

    serializer_class = VoteSerializer

    def get_queryset(self):
        poll_id = self.kwargs['pk']
        choice_id = self.kwargs['choice_pk']
        votes = Vote.objects.filter(poll__id=poll_id, choice__id=choice_id)
        return votes

    def post(self, request, pk, choice_pk):
        voted_by = request.data.get('voted_by')
        data = {'poll': pk, 'choice': choice_pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)