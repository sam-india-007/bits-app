from . import views
from .views import ask
from django.urls import path
from django.conf import settings
from django.contrib.auth import logout
from django.conf.urls import include

from django.conf import settings
from django.conf.urls.static import static

app_name = 'bitsapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('postQ/', ask.as_view(), name='postQ'),
    path('ques/<int:pk>/', views.view_answer, name='view_answer'),
    path('ques/<int:pk>/answer', views.answer, name='answer'),
    path('question_like/<int:pk>', views.QuestionLike, name="question_like"),
    path('profile/<int:pk>', views.profile, name="profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)