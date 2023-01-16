from django.urls import path

from .views import ChoiceListCreateView, VoteListCreateView

app_name = 'choices'
urlpatterns = [
    path('', ChoiceListCreateView.as_view(), name="list-create"),
    path('<int:choice_pk>', VoteListCreateView.as_view(), name="vote-list-create")
]
