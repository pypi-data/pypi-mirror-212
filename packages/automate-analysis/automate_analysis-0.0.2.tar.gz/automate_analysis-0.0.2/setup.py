from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Basic insight generator - EDA'
LONG_DESCRIPTION = 'This package automates and gives you basic visualization of the data, before using the package please install the required lib, the list of lib are mentioned in the __init__.py file in the git hub - https://github.com/Hirshikesh2003/Automate_EDA'

# Setting up
setup(
    name="automate_analysis",
    version=VERSION,
    author="Hirshikesh karan Ahilan",
    author_email="hirshiahilan2003@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=['automate_analysis'],
    #install_requires=['pandas' , 'numpy', 'seaborn', 'plotly.express' , 'ipywidgets'],
    keywords=['python', 'automate', 'automate eda', 'eda', 'analysis', 'data analysis'],
    
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
]
)