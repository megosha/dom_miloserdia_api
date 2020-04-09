from django.contrib import admin
from api import models


# Register your models here.
class ArticleKindAdmin(admin.ModelAdmin):
    list_display = ['kind', 'pk']
    list_display_links = ['kind']
    # save_on_top = True


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'kind', 'date_create']
    search_fields = ['title']
    list_display_links = ['title']
    list_filter = ['kind', 'date_create']
    # save_on_top = True


class PartnerAdmin(admin.ModelAdmin):
    list_display = ['title', 'logo', 'site', 'email', 'address', 'description', 'activity']
    search_fields = ['title', 'email', 'description', 'activity']
    list_display_links = ['title']
    list_editable = ['email', 'description', 'activity']


admin.site.register(models.ArticleKind, ArticleKindAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Partner, PartnerAdmin)