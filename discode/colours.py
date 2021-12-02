from typing import Union

class Colour:
    def __init__(self, value: int):
        self.value = value

    @property
    def r(self):
        return (self.value >> (16)) & 0xff
    
    @property
    def g(self):
        return (self.value >> (8)) & 0xff
    
    @property
    def b(self):
        return (self.value >> (0)) & 0xff

    @classmethod
    def red(cls):
        return cls(0xe74c3c)

    @classmethod
    def green(cls):
        return cls(0x2ecc71)

Color = Colour
