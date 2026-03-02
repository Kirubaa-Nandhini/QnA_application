from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='question_list'),
    path('ask/', views.QuestionCreateView.as_view(), name='question_create'),
    path('<slug:slug>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('<slug:slug>/edit/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('<slug:slug>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
]
