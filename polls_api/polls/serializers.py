from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from users.models import User
from users.serializers import UserSerializer
from .models import Poll, Choice, Vote

def get_object_data(poll_id: int, choice_id: int, vote_id: int) -> tuple:
    poll = Poll.objects.get(id=poll_id)
    choice = Choice.objects.get(id=choice_id)
    voted_by = User.objects.get(id=vote_id)
    return (poll, choice, voted_by)

def get_raw_data(data: dict) -> tuple:
    poll_id = data.get('poll_id')
    choice_id = data.get('choice_id')
    voted_by_id = data.get('voted_by_id')
    assert poll_id, "poll_id is None"
    assert choice_id, "choice_id is None"
    assert voted_by_id, "voted_by_id is None"
    return (poll_id, choice_id, voted_by_id)

def get_data(raw_data) -> dict:
    data = raw_data.copy()
    poll_id, choice_id, voted_by_id = get_raw_data(data)
    poll, choice, voted_by = get_object_data(poll_id, choice_id, voted_by_id)
    data['poll'] = poll.question
    data['choice'] = choice.text
    data['voted_by'] = "user: %s" % voted_by.username
    return data

class VoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vote
        fields = '__all__'

    @property
    def data(self):
        try:
            data =  get_data(super().data)
            return ReturnDict(data, serializer=self)
        except AssertionError as e:
            pass

        return ReturnDict({}, serializer=self)
        
class ChoiceSerializer(serializers.ModelSerializer):
    
    votes = VoteSerializer(many=True, required=False)
    
    class Meta:
        model = Choice
        fields = '__all__'
        depth = 1 

class PollSerializer(serializers.ModelSerializer):
    
    choices = ChoiceSerializer(many=True, required=False, read_only=True)
    created_by = UserSerializer()
    
    class Meta:
        model = Poll
        fields = '__all__'
        depth = 1

class PollCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = '__all__'