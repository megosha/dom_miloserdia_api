import os

from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.contrib.auth.models import User
from django.conf import settings

# Create your views here.
from front import models, forms


def make_context(**kwargs):
    try:
        sett = models.Settings.objects.get()
    except:
        context = {}
    else:
        context = {'settings': sett}
    if kwargs:
        for k, v in kwargs.items():
            context[f'{k}'] = v
    return context


class Index(View):
    def get(self, request):
        # для блока важных партнеров
        important_partners = models.Partner.objects.filter(important=True)[:8]
        # для блоков -Наши партнеры-
        partners = models.Partner.objects.filter(important=False)
        # для блоков Новостей
        articles = models.Article.objects.filter(kind__pk=3, date_publish__lte=timezone.now()).order_by(
            "-date_publish")[:6]
        news_rus = models.Article.objects.filter(kind__pk=2, date_publish__lte=timezone.now()).order_by(
            "-date_publish")[:3]
        news_world = models.Article.objects.filter(kind__pk=1, date_publish__lte=timezone.now()).order_by(
            "-date_publish")[:3]
        context = make_context(important_partners=important_partners,
                               partners=partners,
                               articles=articles,
                               news_rus=news_rus,
                               news_world=news_world, )
        return render(request, 'includes/index.html', context)


"""  ПРОЕКТЫ  """


class CorpRadost(View):
    def get(self, request):
        BASE_DIR = settings.BASE_DIR
        photos1 = os.listdir(os.path.join(BASE_DIR, 'static', 'assets', 'images', 'corp_radost', '1'))
        photos2 = os.listdir(os.path.join(BASE_DIR, 'static', 'assets', 'images', 'corp_radost', '2'))
        photos3 = os.listdir(os.path.join(BASE_DIR, 'static', 'assets', 'images', 'corp_radost', '3'))
        context = make_context(photos1=photos1,
                               photos2=photos2,
                               photos3=photos3)
        return render(request, 'includes/corp_radost.html', context)


class DenMiloserdia(View):
    def get(self, request):
        context = make_context()
        return render(request, 'includes/den_miloserdia.html', context)


class TerritoriaDobra(View):
    def get(self, request):
        BASE_DIR = settings.BASE_DIR
        photos = os.listdir(os.path.join(BASE_DIR, 'static', 'assets', 'images', 'terr_dobra'))
        context = make_context(photos=photos)
        return render(request, 'includes/terriroria_dobra.html', context)


class Mir(View):
    def get(self, request):
        photos = models.Photo.objects.filter(article__pk=123)
        context = make_context(photos=photos)
        return render(request, 'includes/mir.html', context)


"""  ИНФОРМАЦИЯ  """


class Blagodarnost(View):
    def get(self, request):
        context = make_context()
        return render(request, 'includes/blagodarnost.html', context)


class Otchet(View):
    def get(self, request):
        reports = models.Report.objects.all().order_by('-period')
        context = make_context(reports=reports)
        return render(request, 'includes/otchetnost.html', context)


"""  РЕАБИЛИТАЦИЯ  """


class Rehabilitation(View):
    def get(self, request):
        context = make_context()
        return render(request, 'includes/reabilitacia.html', context)


""" ЛЕНТА """


class Lenta(View):
    def get(self, request):
        if 'world' in request.path:
            kind = 1
        elif 'russia' in request.path:
            kind = 2
        else:
            kind = 3
        articles = models.Article.objects.filter(kind__pk=kind, date_publish__lte=timezone.now()).order_by(
            "-date_publish")
        paginator = Paginator(articles, 10)  # 10 posts in each page
        page = request.GET.get('page')
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            articles = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            articles = paginator.page(paginator.num_pages)

        context = make_context(articles=articles,
                               page=page,
                               header=kind)
        request.session['prev_lenta'] = f'{page}'
        return render(request, 'includes/lenta.html', context)


""" СТАТЬЯ """


class Article(View):
    def get(self, request, article_id):
        article = models.Article.objects.filter(pk=article_id, date_publish__lte=timezone.now(),
                                                kind__isnull=False).first()
        if not article:
            return HttpResponseRedirect('/')
        photos = models.Photo.objects.filter(article__pk=article_id)
        prev_page = request.session.pop('prev_lenta') if 'prev_lenta' in request.session else ''
        next_article = models.Article.objects.filter(date_publish__gt=article.date_publish,
                                                     date_publish__lte=timezone.now(),
                                                     kind__pk=article.kind.pk).order_by('date_publish').first()
        prev_article = models.Article.objects.filter(date_publish__lt=article.date_publish,
                                                     date_publish__lte=timezone.now(),
                                                     kind__pk=article.kind.pk).order_by('date_publish').last()
        context = make_context(title=article.title,
                               article=article,
                               photos=photos,
                               prev_page=prev_page,
                               next_article=next_article,
                               prev_article=prev_article)
        return render(request, 'includes/article.html', context)


"""  Партнер  """


class Partner(View):
    def get(self, request, partner_id):
        partner = models.Partner.objects.filter(pk=partner_id).first()
        if not partner:
            return HttpResponseRedirect('/')
        if partner.site:
            return HttpResponseRedirect(partner.site)
        context = make_context(partner=partner)
        return render(request, 'includes/partner.html', context)


"""  Политика безопасности  """


class Policy(View):
    def get(self, request):
        context = make_context()
        return render(request, 'includes/policy.html', context)


class Donate(View):
    def get(self, request):
        context = make_context()
        return render(request, 'includes/donate.html', context)


class Login(View):
    def dispatch(self, request, *args, **kwargs):
        try:
            if self.request.user.is_authenticated:
                return HttpResponseRedirect('/admin_domm')
            else:
                return super(Login, self).dispatch(request)
        except:
            return HttpResponseRedirect('/login')

    def get(self, request):
        form = forms.Login()
        context = make_context(form=form)
        return render(request, 'includes/login.html', context)

    def post(self, request):
        form = forms.Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            pwd = form.cleaned_data['pwd']
            try:
                user = authenticate(username=username, password=pwd)
            except Exception as e:
                print(e)
                return self.get(request)
            login(self.request, user)
            print(user)
            return HttpResponseRedirect('/admin_domm')
        return HttpResponseRedirect('/')


class Logout(View):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return HttpResponseRedirect('/')


def notfound(request, exception=None):
    return redirect('/')
