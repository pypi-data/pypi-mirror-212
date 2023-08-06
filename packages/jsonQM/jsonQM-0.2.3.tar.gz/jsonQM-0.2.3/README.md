# jsonQM

A simple tool to easily make your API endpoint json queries more versatile.

`pip install jsonQM`

## Quick Start

The example model explains how to set up a model and query that model.

*tests/ExampleModel.py*

```py
from jsonQM import *

# Make the model.

# Declare a model serializer
ms = ModelSerializer() # Each model must have its own serializer
class MyModel(Model):
    def __init__(self) -> None:
        # define the structure of the query model:
        self.model = {
            # we have a single query scope/section called functions
            "functions":{}
        }
        # sync/add the model attribute functions to the model
        ms.sync(self)
        
    # Define attributes of the model (argument 2) along with the scope/section they are found in (argument 1)
    @ms.add(["functions"], "repeater")  # This attribute key is "repeater" and can be found in the "functions" dict
    def repeater(self, arg:int):
        # when the attribute is queried it will run this code and return the value
        return ["repeat" for _ in range(arg)]

    # You can use anything as the attribute key that is a valid python dictionary key.
    @ms.add(["functions"], 7)# Keep in mind that if used with json, you are limited to what is a valid json key.
    def number_7(self):
        return "abc"
    


my_cool_api_query_model = MyModel()

#Example query1
print(my_cool_api_query_model.get({
    "functions":{
        # programmed attribute values should be a list containing the function arguments.
        "repeater":[5],
        7:[]
    }
}))

# prints:
# {'functions': {'repeater': ['repeat', 'repeat', 'repeat', 'repeat', 'repeat'], 7: 'abc'}}

#Example query2
print(my_cool_api_query_model.get({
    "functions":{
        # The model will only run/return attributes which have been specified
        "repeater":[5]
    }
}))

# prints:
# {'functions': {'repeater': ['repeat', 'repeat', 'repeat', 'repeat', 'repeat']}}
```

