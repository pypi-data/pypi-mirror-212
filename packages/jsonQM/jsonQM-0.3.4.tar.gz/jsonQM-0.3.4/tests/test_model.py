import unittest

from jsonQM import ModelSerializer, Model

# MODEL
ms = ModelSerializer()  # Each model must have its own serializer
class MyModel(Model):
    def __init__(self) -> None:
        # define the structure of the query model:
        self.model = {
            # we have a single query scope/section called functions
            "functions": {},
            "msg":"test"
        }
        # sync/add the model attribute functions to the model
        ms.sync(self)

    @ms.add(["functions"], "repeater")
    def repeater(self, arg: int):
        return ["repeat" for _ in range(arg)]

    @ms.add(["functions"], 7)
    def number_7(self):
        return "zzz"

    @ms.token()
    @ms.add([], "token")
    def token(self, tok: str):
        if tok == "token":
            return True
        else:
            return False

    @ms.requires_token()
    @ms.add(["functions"], "secret")
    def functions_secret(self):
        return "super secret function message"

    @ms.requires_token()
    @ms.add([], "secret")
    def secret(self):
        return "super secret message"

model = MyModel()
class TestModel(unittest.TestCase):
    def test_token_success(self):
        self.assertEqual(model.get({
            "token": ["token"],
            "functions": {
                "repeater": [5],
                7: [],
                "secret": []
            },
            "secret": [],
            'msg':1
        }), 
        {
            'functions': {
                'repeater': [
                    'repeat', 
                    'repeat', 
                    'repeat', 
                    'repeat', 
                    'repeat'
                ], 
                7: 'zzz', 
                'secret': 'super secret function message'
            }, 
            'secret': 'super secret message', 
            'token': True,
            "msg":"test"
        })

    def test_token_invalid(self):
        self.assertEqual(model.get({
            "token": ["aaa"],
            "functions": {
                "repeater": [5],
                7: [],
                "secret": []
            },
            "secret": [],
            'msg':1
        }), 
        {
            'functions': {
                'repeater': [
                    'repeat', 
                    'repeat', 
                    'repeat', 
                    'repeat', 
                    'repeat'
                ], 
                7: 'zzz', 
                'secret': 'error:token:invalid'
            }, 
            'secret': 'error:token:invalid', 
            'token': False,
            "msg":"test"
        })

    def test_token_missing(self):
        self.assertEqual(model.get({
            "functions": {
                "repeater": [5],
                7: [],
                "secret": []
            },
            "secret": [],
            'msg':1
        }), 
        {
            'functions': {
                'repeater': [
                    'repeat', 
                    'repeat', 
                    'repeat', 
                    'repeat', 
                    'repeat'
                ], 
                7: 'zzz', 
                'secret': 'error:token:missing'
            }, 
            'secret': 'error:token:missing',
            "msg":"test"
        })
    
    def test_default_attribute(self):
        self.assertEqual(model.get({'msg':1}), {'msg': 'test'})


if __name__ == '__main__':
    unittest.main()
