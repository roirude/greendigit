from django.urls import path

from users import views

urlpatterns = [
    path('who_are_you/', views.ChooseUserTypeView.as_view(), name='choose_user_type'),
    path('set_user_type/', views.SetUserTypeView.as_view(), name='set_user_type'),
]
