class Dimension:
    """ tuple(size) """
    _compress_size = None

    def __init__(self, size):
        if isinstance(size, int):
            self.width = size
            self.height = 0
        else:
            self.width = size[0]
            self.height = size[1] if len(tuple(size)) == 2 else 0

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    # compress size
    @property
    def compress_size(self):
        return self._compress_size

    @compress_size.setter
    def compress_size(self, value):
        self._compress_size = value

    def set_compress_size(self, image):
        print("c:{},i:{}".format(self.width, image.size[0]))
        width_percent = (
                self.width / float(image.size[0])
        )
        height_size = int(
            (float(image.size[1]) * float(width_percent))
        )
        self.compress_size = tuple((width_percent, height_size))
