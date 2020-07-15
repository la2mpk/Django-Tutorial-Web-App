from django.urls import path
from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.IndexPageView.as_view(), name='index'),
    path('<int:pk>/', views.DetailPageView.as_view(), name='details'),
    path('<int:pk>/results/', views.ResultsPageView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote')
]
