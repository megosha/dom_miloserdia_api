from django.contrib import admin
from api import models
from django.utils.safestring import mark_safe


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

from imagekit.admin import AdminThumbnail

class PartnerAdmin(admin.ModelAdmin):
    # def image_tag(self, obj):
    #     return format_html('<img src="{}" />'.format(obj.logo.url))

    def icon_tag(self, obj):
        if not (obj.pk and obj.logo):
            return ''
        return mark_safe(f'<img src="{obj.logo.url}" />')

    icon_tag.short_description = 'Icon'
    icon_tag.allow_tags = True
    readonly_fields = ['icon_tag']

    list_display = ['title', 'icon_tag', 'logo', 'site', 'email', 'address', 'description', 'activity']
    search_fields = ['title', 'email', 'description', 'activity']
    list_display_links = ['title']
    # list_editable = ['email', 'description', 'activity']


admin.site.register(models.ArticleKind, ArticleKindAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Partner, PartnerAdmin)