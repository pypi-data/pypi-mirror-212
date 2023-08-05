from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'This sorter is used to sort datasets based on their ASCII Position.'
LONG_DESCRIPTION = "These sorters are based on speed with 3 options: AzuriSorter is the default sorter used. AzuriFastSorter is meant for small datasets, it doesn't perform any corrections. AzuriCorrectiveSorter is a sorter that runs through the data as many times specified it sacrifices speed for accuracy.\nFixes: Fixed Major error in which causes the package to be unusable. Attempts to fix: #2"

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="azurisorting", 
        version=VERSION,
        author="Nathan Hornby",
        author_email="alexmybestcat@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'sorter', 'quick sorter', 'sort', 'fast sort', 'fast', 'corrective sorter', 'corrective', 'auto sorter', 'auto', 'easy sorter', 'easy'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)