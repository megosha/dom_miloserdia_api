from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

# Create your views here.
from front import models


def make_context(**kwargs):
    context = {}
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
        articles = models.Article.objects.filter(kind__pk=3).order_by("-date_create")[:6]
        context = make_context(important_partners=important_partners,
                               partners=partners,
                               articles=articles)
        return render(request, 'includes/index.html', context)


"""  ПРОЕКТЫ  """
class CorpRadost(View):
    def get(self, request):
        context = make_context()
        return render(request, 'includes/corp_radost.html', context)

class DenMiloserdia(View):
    def get(self, request):
        context = make_context()
        return render(request, 'includes/den_miloserdia.html', context)

class TerritoriaDobra(View):
    def get(self, request):
        context = make_context()
        return render(request, 'includes/terriroria_dobra.html', context)


"""  ИНФОРМАЦИЯ  """
class Blagodarnost(View):
    def get(self, request):
        context = make_context()
        return render(request, 'includes/blagodarnost.html', context)

class Otchet(View):
    def get(self, request):
        context = make_context()
        return render(request, 'includes/otchetnost.html', context)

"""  РЕАБИЛИТАЦИЯ  """
class Rehabilitation(View):
    def get(self, request):
        context = make_context()
        return render(request, 'includes/reabilitacia.html', context)

""" ЛЕНТА """
class Lenta(View):
    def get(self, request):
        articles = models.Article.objects.filter(kind__pk=3).order_by("-date_create")
        paginator = Paginator(articles, 10)  # 3 posts in each page
        page = request.GET.get('page')
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            articles = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            articles = paginator.page(paginator.num_pages)

        context = make_context(articles=articles, page=page)
        request.session['prev_lenta'] = f'{page}'
        return render(request, 'includes/lenta.html', context)

""" СТАТЬЯ """
class Article(View):
    def get(self, request, article_id):
        article = models.Article.objects.filter(pk=article_id).first()
        if not article:
            return HttpResponseRedirect('/lenta')
        photos = models.Photo.objects.filter(article__pk=article_id)
        prev_page = request.session.pop('prev_lenta') if 'prev_lenta' in request.session else ''
        context = make_context(article=article, photos=photos, prev_page=prev_page)
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

