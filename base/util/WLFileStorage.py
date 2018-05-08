import os
import uuid

from django.core.files.storage import FileSystemStorage
from django.conf import settings


class UUIDFileStorage(FileSystemStorage):

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(UUIDFileStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        ext = os.path.splitext(name)[1]
        d = os.path.dirname(name)
        fn = str(uuid.uuid1())
        name = os.path.join(d, fn + ext)
        return super(UUIDFileStorage, self)._save(name, content)
