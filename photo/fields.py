import os
from PIL import Image
from django.db.models.fields.files import ImageField, ImageFieldFile


class ThumbnailImageFieldFile(ImageFieldFile):
    # 원본 파일명에 .thumb 를 끼워 넣어 썸네일 파일명을 만든다. (a.png -> a.thumb.jpg)
    def _add_thumb(self, s):
        parts = s.split(".")
        parts.insert(-1, "thumb")
        if parts[-1].lower() not in ('jpeg', 'jpg'):
            parts[-1] = 'jpg'
        return ".".join(parts)

    @property
    def thumb_path(self):
        return self._add_thumb(self.path)

    @property
    def thumb_url(self):
        return self._add_thumb(self.url)

    # 원본을 저장한 뒤, 같은 폴더에 썸네일을 하나 더 만든다.
    def save(self, name, content, save=True):
        super().save(name, content, save)

        img = Image.open(self.path)
        size = (self.field.thumb_width, self.field.thumb_height)
        img.thumbnail(size)
        background = Image.new('RGB', size, (255, 255, 255))
        box = (int((size[0] - img.size[0]) / 2), int((size[1] - img.size[1]) / 2))
        background.paste(img, box)
        background.save(self.thumb_path, 'JPEG')

    # 원본을 지울 때 썸네일도 같이 지운다.
    def delete(self, save=True):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super().delete(save)


class ThumbnailImageField(ImageField):
    attr_class = ThumbnailImageFieldFile

    def __init__(self, verbose_name=None, thumb_width=128, thumb_height=128, **kwargs):
        self.thumb_width, self.thumb_height = thumb_width, thumb_height
        super().__init__(verbose_name, **kwargs)
