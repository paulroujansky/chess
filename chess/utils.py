"""Utils functions and classes."""


class staticproperty(property):
    """Static property.

    A combination of @staticmethod and @property.
    """

    def __get__(self, cls, owner):
        return staticmethod(self.fget).__get__(None, owner)()
