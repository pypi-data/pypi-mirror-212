from typing import Union
from .model import Model

#this is the decorator that serializes the Model
class ModelSerializer:
    def __init__(self) -> None:
        """
        Each Model requires a new `ModelSerializer`.
        """
        self._funcs = []
        self._token_included = False

    def add(self, parent:list, key:Union[int, float, bool, None, str] = tuple()):
        """
        A decorator that adds a model endpoint/function/attribute inside the directory `parent` of the model with a key of `key`.
        """
        def inner(func):
            func._tagged = True
            func._parent = parent
            func._key = key
            return func
        return inner
    
    def token(self):
        """
        A decorator that marks a function as a token handler.
        """
        self._token_included = True
        def inner(func):
            func._token = True
            return func
        return inner

    def requires_token(self):
        """
        A decorator that marks a function as a token handler.
        """
        def inner(func):
            func._requires_token = True
            return func
        return inner

    def sync(self, object:Model):
        """
        Must be called in your Model's `__init__` function after defining your `self.model`.
        You must pass in `self` as the object parameter.  The function call should look like this: `model_serializer_instance.sync(self)`
        """
        if self._token_included:
            object._token = None
        for method_name in dir(object):
            method = getattr(object, method_name)
            if hasattr(method, '_token'):
                object._token_route = (method._parent, method._key)
            if hasattr(method, '_tagged'):
                pointer = object.model
                for index in method._parent:
                    pointer = pointer[index]
                pointer[method._key] = method
