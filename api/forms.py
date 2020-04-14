from django import forms
from django.core.validators import validate_image_file_extension
from django.utils.translation import gettext as _


from api.models import Article, Photo


class ShowAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            "kind",
            "title",
            "content",
            "video",
        )

    photos = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        label=_("Добавить фотографии"),
        required=False,
    )

    def clean_photos(self):
        """Make sure only images can be uploaded."""
        for upload in self.files.getlist("photos"):
            validate_image_file_extension(upload)

    def save_photos(self, article):
        """Process each uploaded image."""
        for upload in self.files.getlist("photos"):
            photo = Photo(article=article, photo=upload)
            photo.save()