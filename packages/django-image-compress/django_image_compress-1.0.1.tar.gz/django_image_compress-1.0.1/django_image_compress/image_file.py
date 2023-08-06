import sys

from PIL import Image
import os
import uuid

from django.core.files.uploadedfile import InMemoryUploadedFile


class ImageFile:
    _name = None

    def __init__(self, image):
        # set image
        self.image = Image.open(image).convert('RGB')
        # set extension image
        self.extension = os.path.splitext(image.name)[1]

    """ image """

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    """ extension """

    @property
    def extension(self):
        return self._extension

    @extension.setter
    def extension(self, value):
        self._extension = value

    """ set image name"""

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def set_name(self, name):
        if not name:
            self.name = "{}{}".format(uuid.uuid4().hex[:8].upper(), self.extension)
        else:
            self.name = "{}{}".format(name, self.extension)

    def save_file(self, name, output):
        self.set_name(name)
        img = InMemoryUploadedFile(
            output, 'ImageField', "{}".format(
                self.name
            ), 'image/jpeg', sys.getsizeof(output), None
        )
        return img
