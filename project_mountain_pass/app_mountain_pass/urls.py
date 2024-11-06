from django.urls import path
from .views import submit_data, get_pass, edit_pass, user_passes

urlpatterns = [
    path('submit_data/', submit_data, name='submit_data'),  # Создание нового перевала
    path('submit_data/<int:id>/', get_pass, name='get_pass'),  # Получение перевала по id
    path('submit_data/<int:id>/edit/', edit_pass, name='edit_pass'),  # Редактирование перевала по id
    path('user_passes/', user_passes, name='user_passes'), # Получение перевалов пользователя по email
]
