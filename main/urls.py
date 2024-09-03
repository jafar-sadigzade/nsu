from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name=''),
    path('news', views.news_request, name='news'),
    path('news-details/<int:news_id>', views.news_details, name='news_detail'),
    path('events', views.events_request, name='events'),
    path('event-details/<int:event_id>', views.event_details, name='event_details'),
    path('contact', views.contact, name='contact'),
]
