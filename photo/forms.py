from django.forms import inlineformset_factory
from photo.models import Album, Photo

photoLnlineFormSet = inlineformset_factory(Album, Photo, fields=['image', 'title', 'description'], extra=2)