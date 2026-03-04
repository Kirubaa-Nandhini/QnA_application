from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='question_list'),
    path('ask/', views.QuestionCreateView.as_view(), name='question_create'),
    path('<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('<int:pk>/edit/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
]
