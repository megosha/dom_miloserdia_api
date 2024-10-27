from django import forms
from django.core.validators import validate_image_file_extension
from django.utils.translation import gettext as _


from front.models import Article, Photo


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ShowAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            "kind",
            "instagram_id",
            "title",
            "date_publish",
            "cover",
            "content",
            # "video",
            "videolink",
            "videocover",
        )

    photos = MultipleFileField(
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

class Login(forms.Form):
    login = forms.CharField(label="Имя пользователя", max_length=100,
                               widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    pwd = forms.CharField(label="Пароль", max_length=64,
                               widget=forms.PasswordInput(attrs={'type':"password", 'placeholder': 'Пароль'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})