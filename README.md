# qtwidgets
Collection of custom widgets for qt python 


## Installation from github
    pip install git+https://github.com/MikeSmithLabTeam/qtwidgets
    
## Pyside2 is a dependency but is better installed with conda
    conda install -c conda-forge pyside2
    
## Updating if already installed
    pip install --upgrade git+https://github.com/MikeSmithLabTeam/qtwidgets
    
## To add as a dependency to another pip repository
Add the following argument to setup.py setuptools.setup()

    dependency_links=['https://github.com/MikeSmithLabTeam/qtwidgets/tarball/repo/master#egg=package-1.0'],
