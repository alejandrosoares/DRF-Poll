from django.urls import path, include

from .views import poll_list, poll_detail
from .views import PollListView, PollCreateView, PollDetailDeleteView

app_name = 'polls'
urlpatterns = [
    path('api', poll_list, name="list"),
    path('api/<int:pk>', poll_detail, name="detail"),
    path('', PollListView.as_view(), name="api-list"),
    path('create', PollCreateView.as_view(), name="api-create"),
    path('<int:pk>', PollDetailDeleteView.as_view(), name="api-detail-delete"),
    path('<int:pk>/choices/', include('polls.urls-choices'))
]
