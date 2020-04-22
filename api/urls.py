from django.urls import path

from api import views, ajax

from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register('partnersall', views.Partners)

urlpatterns = [
    path('feedback/', ajax.Feedback.as_view()),

]
urlpatterns.extend(router.urls)
