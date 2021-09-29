from django.urls import path
from .views import AgentListView, AgentCreateView

urlpatterns= [
    path('', AgentListView.as_view(), name="agent_List"),
    path('create/', AgentCreateView.as_view(), name="agent_create"),
]