
class Model:
    def __init__(self) -> None:
        self.model = {}

    def _get(self, query:dict, model = {}):
        compiled_query = {}
        for key, value in query.items():
            if type(value) == dict:
                compiled_query[key] = self._get(value, model[key])
            elif type(value) == list:
                compiled_query[key] = model[key](*value)
            else:
                compiled_query[key] = value

        return compiled_query

    def get(self, query:dict):
        """
        Used to make queries to your `Model`.
        """
        return self._get(query, self.model)