from setuptools import setup, find_packages

VERSION = '0.3.4' 
DESCRIPTION = 'A simple tool to easily make your API endpoint json queries more versatile.'
file = open("README.md", 'r')
LONG_DESCRIPTION = file.read()
file.close()

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="jsonQM", 
        version=VERSION,
        author="William A. Lim",
        author_email="william.lim@csu.fullerton.edu",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'json', 'request', 'query', 'model'],
        classifiers= [
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent"
        ],
        project_urls={
            'Source': 'https://github.com/FrewtyPebbles/jsonQM',
            'Tracker': 'https://github.com/FrewtyPebbles/jsonQM/issues'
        }
)
