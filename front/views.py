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
        important_partners = models.Partner.objects.filter(important=True)
        context = make_context(important_partners=important_partners)
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
