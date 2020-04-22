from django.urls import re_path, path

from front import views

urlpatterns = [
    path('', views.Index.as_view()),
    path('corp_radost/', views.CorpRadost.as_view()),
    path('den_miloserdia/', views.DenMiloserdia.as_view()),
    path('territoria_dobra/', views.TerritoriaDobra.as_view()),
    path('blagodarnost/', views.Blagodarnost.as_view()),
    path('otchet/', views.Otchet.as_view()),
    path('rehabilitation/', views.Rehabilitation.as_view()),
    path('partner/<int:partner_id>', views.Partner.as_view()),
    re_path('^lenta/world', views.Lenta.as_view()),
    re_path('^lenta/russia', views.Lenta.as_view()),
    re_path('^lenta/', views.Lenta.as_view()),
    path('article/<int:article_id>', views.Article.as_view()),
    path('policy/', views.Policy.as_view()),

]
