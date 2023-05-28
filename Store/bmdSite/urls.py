from django.urls import path, include
from . import views
urlpatterns = [
    
    path('', views.MainPageView.as_view(), name="main-page"),
    path('store<slug:slug>', views.StoreView.as_view(), name="store-page" ),
    path('box/', views.BoxView.as_view(), name="box-page"),
    path('boxx/', views.Add_to_session, name="add-session")
]