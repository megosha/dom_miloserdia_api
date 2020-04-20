from django.contrib import admin
from django.template.loader import get_template
from django.utils.translation import gettext as _

from front import models
from django.utils.safestring import mark_safe
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from front.forms import ShowAdminForm


# Register your models here.
class ArticleKindAdmin(admin.ModelAdmin):
    list_display = ['kind', 'pk']
    list_display_links = ['kind']
    # save_on_top = True


class ShowPhotoInline(admin.TabularInline):
    model = models.Photo
    fields = ("showphoto_thumbnail",)
    readonly_fields = ("showphoto_thumbnail",)
    max_num = 0
    def showphoto_thumbnail(self, instance):
        """A (pseudo)field that returns an image thumbnail for a show photo."""
        tpl = get_template("front/admin/show_thumbnail.html")
        return tpl.render({"photo": instance.photo})
    showphoto_thumbnail.short_description = _("Thumbnail")

class ArticleAdmin(admin.ModelAdmin):
    def cover_tag(self, obj):
        if not (obj.pk and obj.cover):
            return ''
        return mark_safe(f'<a href="{obj.cover.url}" target="_blank"><img src="{obj.cover.url}" height="70px"/></a>')

    cover_tag.short_description = 'Обложка'
    cover_tag.allow_tags = True
    readonly_fields = ['cover_tag', "date_create",]

    list_display = ['title', 'kind', 'date_create', 'cover_tag']
    search_fields = ['title']
    list_display_links = ['title']
    list_filter = ['kind', 'date_create']
    # readonly_fields = ("date_create",)

    form = ShowAdminForm
    inlines = [ShowPhotoInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.save_photos(form.instance)


class PartnerAdmin(admin.ModelAdmin, DynamicArrayMixin):
    def icon_tag(self, obj):
        if not (obj.pk and obj.logo):
            return ''
        return mark_safe(f'<a href="{obj.logo.url}" target="_blank"><img src="{obj.logo.url}" height="50px"/></a>')

    icon_tag.short_description = 'Логотип'
    icon_tag.allow_tags = True
    readonly_fields = ['icon_tag']

    list_display = ['pk', 'title', 'icon_tag', 'important', 'site', 'email', 'address', 'description', 'activity']
    search_fields = ['title', 'email', 'description', 'activity']
    list_display_links = ['title']
    list_filter = ['important',]
    # list_editable = ['important']

class ReportAdmin(admin.ModelAdmin):
    list_display = ['period', 'title', 'file']
    list_display_links = ['period']

admin.site.register(models.ArticleKind, ArticleKindAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Partner, PartnerAdmin)
admin.site.register(models.Report, ReportAdmin)