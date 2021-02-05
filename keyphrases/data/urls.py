from django.urls import path

from data import views

urlpatterns = [
    path('', views.text_save, name='text_save'),
    path('all_texts/', views.all_texts, name='all_texts'),
    # path('key_ph/<int:pk>/', views.key_ph),
    path('text_page/<int:pk>/', views.text_page, name='text_page'),
    path('top', views.top_keywords, name='top_keywords')
]