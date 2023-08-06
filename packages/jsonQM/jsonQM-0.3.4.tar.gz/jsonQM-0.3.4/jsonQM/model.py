
from typing import Callable


class Model:
    def __init__(self) -> None:
        self.model = {}

    def _get(self, query:dict, model:dict = {}, token_result:bool = None):
        compiled_query = {}
        for key, value in query.items():
            if type(value) == dict:
                compiled_query[key] = self._get(value, model[key])
            elif type(value) == list:
                if hasattr(model[key], '_requires_token'):
                    if hasattr(self, '_token'):
                        if self._token == True:
                            compiled_query[key] = model[key](*value)
                        elif self._token == False:
                            compiled_query[key] = "error:token:invalid"
                        else:
                            compiled_query[key] = "error:token:missing"
                    else:
                        compiled_query[key] = "error:token:missing"
                elif hasattr(model[key], '_token'):
                    compiled_query[key] = token_result
                else:
                    compiled_query[key] = model[key](*value)
            elif key in model.keys():
                if type(model[key]) != Callable:
                    compiled_query[key] = model[key]
            else:
                compiled_query[key] = value

        return compiled_query

    def get(self, query:dict):
        """
        Used to make queries to your `Model`.
        """
        token_result = None
        if hasattr(self, '_token') and hasattr(self, '_token_route'):
            token_func = self.model
            args = query
            for attr in self._token_route[0]:
                token_func = token_func[attr]
                args = args[attr]
            if self._token_route[1] in token_func.keys() and self._token_route[1] in args.keys():
                token_result = token_func[self._token_route[1]](*args[self._token_route[1]])
                self._token = token_result
            else:
                self._token = token_result
        response = self._get(query, self.model, token_result)
        if hasattr(self, '_token'):
            self._token = None
        return response