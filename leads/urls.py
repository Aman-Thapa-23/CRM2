from django.urls import path
# from .views import (lead_create, lead_list, lead_delete, lead_details, lead_update)
from .views import (LeadListView, LeadDetailsView, LeadCreateView, LeadUpdateView, LeadDeleteView)

#urls of function based view
# urlpatterns = [
#     path('', views.lead_list, name="lead_list"),
#     path('<int:pk>/',views.lead_details, name="lead_details"),
#     path('<int:pk>/update/',views.lead_update, name="lead_update"),
#     path('create/', views.lead_create, name="lead_create"),
#     path('<int:pk>/delete/',views.lead_delete, name="lead_delete"),
# ]

#urls of class based view. In this project view is working through class based view.
urlpatterns = [
    path('', LeadListView.as_view(), name="lead_list"),
    path('<int:pk>/', LeadDetailsView.as_view(), name="lead_details"),
    path('<int:pk>/update/',LeadUpdateView.as_view(), name="lead_update"),
    path('create/', LeadCreateView.as_view(), name="lead_create"),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name="lead_delete"),
]