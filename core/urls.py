from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('event/<int:event_id>/register/', views.register_event, name='register_event'),
    path('my-events/', views.MyEventsListView.as_view(), name='my_events'),
    path('registration/<int:registration_id>/unregister/', views.unregister_event, name='unregister_event'),
    path('signup/', views.signup, name='signup'),
]



