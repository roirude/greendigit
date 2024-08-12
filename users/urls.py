from django.urls import path

from users import views

urlpatterns = [
    path('who_are_you/', views.ChooseUserTypeView.as_view(), name='choose_user_type'),
    path('set_user_type/', views.SetUserTypeView.as_view(), name='set_user_type'),
    path('fm/dashboard/', views.FarmerDashboardView.as_view(), name='farmer_dashboard'),
    path('csm/dashboard/', views.ConsumerDashboardView.as_view(), name='consumer_dashboard'),
    path("choose_your_profile/", views.choose_user_type, name="choose_your_social_profile"),
]
