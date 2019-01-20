class Cell:
    def __init__(self, x, y):
        self.x_coord = x
        self.y_coord = y
        self.is_base = False
        self.is_free = True
        self.is_shape = False
    def make_shape(self):
        self.is_shape=True
    def make_base(self):
        self.is_shape=True
        self.is_base=True
    def make_free(self):
        self.is_free=True
        self.is_shape=False
        self.is_base=False
    def make_froze(self):
        self.is_free=False
        self.is_shape=False
        self.is_base=False
