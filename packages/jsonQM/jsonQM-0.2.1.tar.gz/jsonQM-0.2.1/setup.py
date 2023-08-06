from setuptools import setup, find_packages

VERSION = '0.2.1' 
DESCRIPTION = 'A simple tool to easily make your API endpoint json queries more versatile.'
LONG_DESCRIPTION = 'This module allows you to make your API endpoints more versatile by binding response functions to different entries on your json request similar to GraphQL.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="jsonQM", 
        version=VERSION,
        author="William A. Lim",
        author_email="william.lim@csu.fullerton.edu",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'json', 'request', 'query', 'model'],
        classifiers= [
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent"
        ]
)
