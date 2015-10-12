from flask import current_app

__all__ = ['basecollection', 'errors']
__author__ = 'ievans3024'

API_URI_PREFIX = current_app.config.get('API_ROOT') or '/api'


class APIType(object):
    """Descriptor for properties that need to a class or a subclass of such."""

    def __init__(self, cls):
        if isinstance(cls, type):
            self.cls = cls
        else:
            raise TypeError("Parameter 'cls' must be a class.")

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            if self.get_own_name(owner) in instance.__dict__.keys():
                return instance.__dict__.get(self.get_own_name(owner))
            else:
                raise AttributeError(
                    "'{cls}' object has no attribute '{name}'".format(
                        cls=owner.__name__,
                        name=self.get_own_name(owner)
                    )
                )

    def __set__(self, instance, value):
        if instance:
            if not ((value is self.cls) or (issubclass(value, self.cls))):
                raise ValueError(
                    "Value must be {cls} or a subclass of it.".format(
                        cls=".".join([self.cls.__module__, self.cls.__name__])
                    )
                )
            instance.__dict__[self.get_own_name(type(instance))] = value

    def __delete__(self, instance):
        if instance:
            del instance.__dict__[self.get_own_name(type(instance))]

    def get_own_name(self, owner):
        for attr in dir(owner):
            if getattr(owner, attr) is self:
                return attr


class APIField(APIType):
    """Descriptor for properties that need to be an instance of a class or subclass of such."""

    def __set__(self, instance, value):
        if not isinstance(value, self.cls):
            raise TypeError(
                "Value must be an instance of {cls} or one of its subclasses.".format(
                    cls=".".join([self.cls.__module__, self.cls.__name__])
                )
            )
        instance.__dict__[self.get_own_name(type(instance))] = value