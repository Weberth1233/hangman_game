from django.urls import path
from . import views

urlpatterns = [
    path('token/', views.get_csrf_token, name='get_csrf_token'),
    path('login/', views.api_login, name='user_login'),
    path('words/', views.word_list, name='word_list'),
    path('random_word/', views.word_random_game, name='word_random_game'),
    path('start_new_game/', views.start_new_game, name='start_new_game')
]